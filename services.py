# ============================================================================
# FILE: services.py
# ============================================================================
import io
import json
from groq import Groq
from PyPDF2 import PdfReader
from docx import Document
from typing import Dict, Any

class ResumeParserService:
    def __init__(self, groq_api_key: str, model_name: str = "llama-3.3-70b-versatile"):
        self.client = Groq(api_key=groq_api_key)
        self.model_name = model_name
    
    def extract_text_from_pdf(self, content: bytes) -> str:
        """Extract text from PDF file"""
        pdf_file = io.BytesIO(content)
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    def extract_text_from_docx(self, content: bytes) -> str:
        """Extract text from DOCX file"""
        doc_file = io.BytesIO(content)
        doc = Document(doc_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    async def parse_resume(self, content: bytes, file_extension: str) -> Dict[str, Any]:
        """
        Parse resume using Groq AI
        """
        # Extract text based on file type
        if file_extension.lower() == '.pdf':
            text = self.extract_text_from_pdf(content)
        elif file_extension.lower() in ['.docx', '.doc']:
            text = self.extract_text_from_docx(content)
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")
        
        # Create prompt for AI
        prompt = f"""
You are an expert resume parser. Extract the following information from the resume text and return it as a JSON object.

IMPORTANT: Return ONLY valid JSON without any markdown formatting, code blocks, or explanations.

Extract these fields:
1. name: Full name of the candidate
2. email: Email address
3. phone: Phone number
4. total_years_experience: Total years of work experience (as a number, calculate from all jobs mentioned)
5. last_job_title: Job title of the most recent position
6. last_job_company: Company name of the most recent position
7. last_job_duration: Duration of the most recent job (e.g., "Jan 2020 - Present")
8. highest_degree: Highest educational degree (e.g., "Bachelor's in Computer Science")
9. university: Name of university/college
10. graduation_year: Year of graduation
11. special_highlights: Any notable achievements, awards, certifications, volunteer work, or unique experiences (e.g., "2x National Finalist", "NGO volunteer supporting underprivileged children", "Published researcher")
12. skills: Comma-separated list of technical and professional skills

If any field is not found, use null.

Resume Text:
{text}

Return the result as a JSON object with the exact field names specified above.
"""
        
        # Call Groq API
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a precise resume parser that extracts structured data and returns only valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            # Parse the response
            result_text = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()
            
            # Parse JSON
            parsed_data = json.loads(result_text)
            
            # Ensure all required fields exist
            default_data = {
                "name": None,
                "email": None,
                "phone": None,
                "total_years_experience": None,
                "last_job_title": None,
                "last_job_company": None,
                "last_job_duration": None,
                "highest_degree": None,
                "university": None,
                "graduation_year": None,
                "special_highlights": None,
                "skills": None
            }
            
            default_data.update(parsed_data)
            return default_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse AI response as JSON: {e}")
        except Exception as e:
            raise ValueError(f"Error parsing resume with AI: {e}")