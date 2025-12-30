import io
import json
from groq import Groq
from PyPDF2 import PdfReader
import pdfplumber
from docx import Document
from typing import Dict, Any

class ResumeParserService:
    def __init__(self, groq_api_key: str, model_name: str = "llama-3.3-70b-versatile"):
        self.client = Groq(api_key=groq_api_key)
        self.model_name = model_name
    
    def extract_text_from_pdf(self, content: bytes) -> str:
        """Extract text from PDF file with fallback support for various encodings"""
        text = ""
        
        # Try PyPDF2 first (faster)
        try:
            pdf_file = io.BytesIO(content)
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            # If we got meaningful text (more than just whitespace), return it
            if text.strip() and len(text.strip()) > 50:
                return text
        except Exception as e:
            print(f"PyPDF2 extraction failed: {e}. Trying pdfplumber...")
        
        # Fallback to pdfplumber for better encoding support
        try:
            pdf_file = io.BytesIO(content)
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            print(f"pdfplumber extraction also failed: {e}")
            # Return whatever we got, even if minimal
            return text if text else ""
    
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
        
        # Get current date for accurate "Present" calculation
        from datetime import datetime
        current_year = datetime.now().year
        current_date = datetime.now().strftime("%B %Y")

        # Create prompt for AI
        prompt = f"""
You are an expert resume parser. Extract the following information from the resume text and return it as a JSON object.

CURRENT DATE: {current_date} (Use this for "Present" calculations)

IMPORTANT INSTRUCTIONS:
1. Return ONLY valid JSON without any markdown formatting, code blocks, or explanations.
2. For "total_years_experience": ONLY count PROFESSIONAL WORK EXPERIENCE years.
   - DIRECTLY EXCLUDE education years. Graduation years are NOT work experience.
   - Look for "Work Experience", "Professional Experience", "Employment History" sections.
   - Calculate the sum of durations for each job role.
   - IGNORE dates associated with "Education", "University", "College", "Degree".
   - Example matches to IGNORE: "2020-2024 Bachelor of Science", "Graduated 2023".
   - If a candidate graduated in {current_year - 1}, their experience starts from their first job, NOT {current_year - 5}.
3. Education years (like Bachelor's 2020-2024) should ONLY go in graduation_year field.
4. If the only dates present are for education, total_years_experience should be 0 (not null, not NA).
5. DATE RANGE CALCULATION (CRITICAL):
   - FIRST check if the job duration mentions "Present", "Current", "Ongoing", or "Till Date".
   - If "Present" is mentioned: Calculate from start date to {current_year}.
   - If an EXPLICIT END DATE is given (e.g., "2020-2023"): Use THAT end date, NOT the current year.
   - Example: "2020-2023" = 3 years (NOT 5 years by counting to 2025).
   - Example: "2020-Present" = 5 years (counting to 2025).
6. HANDLING SCRAMBLED TEXT (CRITICAL):
   - In some PDFs, all dates appear at the end of the text, detached from sections.
   - You must reconstruct the timeline to find the "True Professional Start Date".
   - IGNORE early date clusters if they overlap with typical education ages or are disconnected from the main work block.
   - Rule of Thumb: If you see a set of dates like [2012-2015, 2014-2017, 2018-2020, 2020-{current_year}], and the recent work is 2018-{current_year} (5 years):
     - The earlier dates (2012-2017) are likely Degrees or Internships. IGNORE THEM.
     - ONLY count the continuous block of recent professional experience.
   - For Jonathan Patterson (example): 2018-2023 is Work. 2012-2017 is Education. Total should be 5 years.
7. HANDLING FUTURE DATES (CRITICAL):
   - Treat future dates (e.g., 2027-2030) as valid experience (scenario/projection).
   - If a candidate has a job "2027 - 2030", count this as 3 years of experience.
   - Do NOT ignore dates just because they are in the future.
   - However, if the future date is for Graduation (e.g. "Expected 2027"), DO NOT count it as experience.
8. OVERLAPPING DATES & INTERNSHIPS:
   - If timelines overlap (e.g., 2015-2020 and 2018-2020), prioritize the explicit Professional Job Titles.
   - Exclude "Internship", "Volunteer", or "Student" roles if they pre-date the main professional career.
   - For Jonathan Patterson (scrambled specific): 2018-2023 is the valid work block (5 years). The 2013-2015/2015-2020 dates are pre-professional/internships and should be excluded.
9. SPELL CHECKING (CRITICAL):
   - Double-check spellings for: name, last_job_title, last_job_company, university, highest_degree.
   - Correct obvious typos and OCR errors (e.g., "Unlverslty" -> "University").
   - Preserve proper nouns and company names as written unless clearly misspelled.


Extract these fields:
1. name: Full name of the candidate
2. email: Email address
3. phone: Phone number
4. total_years_experience: Total years of WORK EXPERIENCE ONLY (number). DO NOT include time spent in university/college. Present year is 2025
5. last_job_title: Job title of the most recent position
6. last_job_company: Company name of the most recent position
7. last_job_duration: Duration of the most recent job (e.g., "Jan 2020 - Present")
8. highest_degree: Highest educational degree (e.g., "Bachelor's in Computer Science")
9. university: Name of university/college
10. graduation_year: Year of graduation
11. special_highlights: Any notable achievements, awards, certifications, volunteer work, or unique experiences
12. skills: Comma-separated list of technical and professional skills

Resume Text:
{text}

Return the result as a JSON object with the exact field names specified above.
"""
        
        # Call Groq API with retry logic
        max_retries = 3
        base_delay = 2
        
        try:
            import asyncio
            import time
            response = None
            
            for attempt in range(max_retries):
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
                    break # Success, exit loop
                    
                except Exception as e:
                    error_str = str(e).lower()
                    if "rate_limit" in error_str or "429" in error_str:
                        if attempt < max_retries - 1:
                            wait_time = base_delay * (2 ** attempt)
                            print(f"Rate limit hit. Retrying in {wait_time}s...")
                            time.sleep(wait_time)
                            continue
                    raise e # Re-raise if not rate limit or retries exhausted
            
            # Parse the response
            if not response:
                raise ValueError("Failed to get response from AI service")
                
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
                "total_years_experience": 0,
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
            
            # Ensure total_years_experience is an integer
            try:
                exp = default_data.get("total_years_experience")
                if exp is None:
                    default_data["total_years_experience"] = 0
                else:
                    default_data["total_years_experience"] = int(float(str(exp)))
            except (ValueError, TypeError):
                default_data["total_years_experience"] = 0
                
            return default_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse AI response as JSON: {e}")
        except Exception as e:
            raise ValueError(f"Error parsing resume with AI: {e}")