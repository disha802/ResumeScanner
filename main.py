from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import os
from dotenv import load_dotenv
from tortoise import Tortoise
from tortoise.transactions import in_transaction
from contextlib import asynccontextmanager
import uvicorn
import io
import pandas as pd

from models import Resume
from services import ResumeParserService
from database import init_db, close_db

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()

app = FastAPI(
    title="Resume Parser API",
    description="AI-powered bulk resume parsing with Groq and Neon DB",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize parser service
parser_service = ResumeParserService(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

@app.get("/")
async def root():
    return {"message": "Resume Parser API is running"}

@app.get("/test/groq")
async def test_groq():
    """Test if Groq API is working"""
    try:
        response = parser_service.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": "Say 'Hello, Groq is working!'"}
            ],
            max_tokens=50
        )
        return {
            "status": "success",
            "message": response.choices[0].message.content
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.post("/upload/bulk")
async def upload_bulk_resumes(files: List[UploadFile] = File(...)):
    """
    Upload multiple resume files (PDF, DOCX) for bulk processing
    Uses transactions to ensure data integrity
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    # Validate file types
    allowed_extensions = {'.pdf', '.docx', '.doc'}
    results = {
        "total": len(files),
        "successful": 0,
        "failed": 0,
        "errors": [],
        "resumes": []
    }
    
    for file in files:
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            results["failed"] += 1
            results["errors"].append({
                "filename": file.filename,
                "error": f"Unsupported file type: {file_ext}"
            })
            continue
        
        # Use transaction for each file to ensure atomicity
        # If anything fails, the database insert is rolled back
        connection = Tortoise.get_connection("default")
        
        try:
            # Start transaction with proper connection
            async with in_transaction(connection_name="default") as conn:
                # Read file content
                content = await file.read()
                print(f"Processing file: {file.filename}, size: {len(content)} bytes")
                
                # Parse resume using AI
                parsed_data = await parser_service.parse_resume(content, file_ext)
                print(f"Parsed data for {file.filename}: {parsed_data.get('name', 'NO NAME')}")
                
                # Save to database (within transaction)
                # If this fails, transaction rolls back automatically
                resume = await Resume.create(**parsed_data, using_db=conn)
                print(f"Successfully saved resume ID: {resume.id}")
                
                results["successful"] += 1
                results["resumes"].append({
                    "id": resume.id,
                    "name": resume.name,
                    "filename": file.filename
                })
            # Transaction commits here if everything succeeded
            
        except Exception as e:
            # Transaction automatically rolled back on exception
            print(f"ERROR processing {file.filename}: {str(e)}")
            import traceback
            traceback.print_exc()
            results["failed"] += 1
            results["errors"].append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return JSONResponse(content=results, status_code=200)

@app.get("/resumes")
async def get_all_resumes(skip: int = 0, limit: int = 100):
    """
    Get all parsed resumes from database
    """
    resumes = await Resume.all().offset(skip).limit(limit)
    return {
        "count": len(resumes),
        "resumes": [await resume.to_dict() for resume in resumes]
    }

@app.get("/resumes/{resume_id}")
async def get_resume(resume_id: int):
    """
    Get a specific resume by ID
    """
    resume = await Resume.get_or_none(id=resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return await resume.to_dict()

@app.delete("/resumes/{resume_id}")
async def delete_resume(resume_id: int):
    """
    Delete a specific resume
    """
    resume = await Resume.get_or_none(id=resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    await resume.delete()
    return {"message": "Resume deleted successfully"}

@app.delete("/resumes")
async def delete_all_resumes():
    """
    Delete all resumes
    """
    await Resume.all().delete()
    return {"message": "All resumes deleted successfully"}

@app.get("/export/excel")
async def export_to_excel():
    """
    Export all resumes to Excel format
    """
    try:
        # Get all resumes
        resumes = await Resume.all()
        
        if not resumes:
            raise HTTPException(status_code=404, detail="No resumes found to export")
        
        # Convert to list of dictionaries
        data = []
        for resume in resumes:
            data.append({
                "ID": resume.id,
                "Name": resume.name,
                "Email": resume.email,
                "Phone": resume.phone,
                "Total Experience (Years)": resume.total_years_experience,
                "Last Job Title": resume.last_job_title,
                "Last Job Company": resume.last_job_company,
                "Last Job Duration": resume.last_job_duration,
                "Highest Degree": resume.highest_degree,
                "University": resume.university,
                "Graduation Year": resume.graduation_year,
                "Skills": resume.skills,
                "Special Highlights": resume.special_highlights,
                "Created At": resume.created_at.strftime("%Y-%m-%d %H:%M:%S") if resume.created_at else None
            })
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Create Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Resumes')
        
        output.seek(0)
        
        # Return as downloadable file
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=resumes_export.xlsx"
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting to Excel: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)