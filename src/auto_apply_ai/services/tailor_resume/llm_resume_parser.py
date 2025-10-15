import re
import json
import fitz
from langchain_core.language_models import LLM
import spacy
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from pydantic import BaseModel, ValidationError
from openai import OpenAI
from dataclasses import dataclass

from auto_apply_ai.services.tailor_resume.tailor_resume_scm import Resume, Experience, Basics
from dotenv import load_dotenv
load_dotenv()


# ========== PDF Text Extraction ==========
def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF using PyMuPDF"""
    doc = fitz.open(pdf_path)
    parts = []
    for page in doc:
        parts.append(page.get_text("text"))
    doc.close()
    text = "\n".join(parts)
    # Normalize whitespace
    text = re.sub(r"\r", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ========== Complete LLM Parser ==========
class LLMResumeParser:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        """
        Initialize LLM parser
        
        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY env var)
            model: Model to use.
        """
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()
        self.model = model
    
    def create_extraction_prompt(self, resume_text: str) -> str:
        """Create detailed prompt for resume extraction"""
        return f"""You are an expert resume parser. Extract ALL information from this resume into a structured JSON format.

CRITICAL INSTRUCTIONS:
1. Extract EVERY work experience as a separate object with sequential IDs (exp_1, exp_2, etc.)
2. For each experience, extract ALL bullet points/achievements as separate array items
3. Keep bullet points as individual strings - DO NOT combine them
4. Extract ALL skills as separate items in the skills array
5. If a field is missing or unclear, use empty string "" or null
6. Maintain the original meaning and details - do not summarize or lose information

JSON Schema (STRICT - follow exactly):
{{
  "basics": {{
    "name": "Full Name",
    "email": "email@domain.com",
    "phone": "+1234567890" or null,
    "location": "City, Country" or null
  }},
  "summary": "Complete professional summary paragraph from the resume",
  "skills": ["Skill 1", "Skill 2", "Skill 3", ...],
  "experience": [
    {{
      "id": "exp_1",
      "company": "Company Name",
      "title": "Job Title",
      "start": "MM/YYYY or YYYY",
      "end": "MM/YYYY or YYYY or Present",
      "bullet_point": [
        "First achievement or responsibility",
        "Second achievement or responsibility",
        "Third achievement or responsibility"
      ]
    }},
    {{
      "id": "exp_2",
      ...
    }}
  ],
  "education": "Degree, Institution, Year | Another Degree, Institution, Year",
  "certifications": "Cert 1, Issuer, Year | Cert 2, Issuer, Year" or null,
  "projects": "Project 1: Description | Project 2: Description" or null
}}

EXTRACTION RULES:
- basics: 
  * Extract exact name, email, phone, location from contact information
  * phone and location can be null if not found
  * email is required - find it anywhere in the document
  
- summary: 
  * PRIORITY 1: Look for "Summary", "Professional Summary", "Profile", "About", "Objective" sections
  * Extract the COMPLETE summary text from that section (2-5 sentences typically)
  * ONLY if no summary section exists: Create a brief 2-sentence summary from work experience highlights
  * Do NOT summarize if a summary section exists - use the exact text

- skills: 
  * PRIORITY 1: Look for "Skills", "Technical Skills", "Competencies", "Technologies" sections
  * Extract ALL skills listed in that section as individual items
  * Include programming languages, frameworks, tools, methodologies, databases, etc.
  * ONLY if no skills section exists: Extract skills mentioned in experience descriptions
  * Keep skills as listed - do not group or categorize

- experience: 
  * Create separate objects for EACH job
  * bullet_point should be an array with each achievement/responsibility as a separate string
  * Keep all details from the resume
  * Use start/end dates in MM/YYYY or YYYY format
  * Extract dates from anywhere near the job title/company

- education: 
  * Combine all education entries with " | " separator
  * Include degree, institution, year, and grade/GPA if mentioned

- certifications: Extract if present, use null if none
- projects: Extract if present, use null if none

Resume Text:
{resume_text}

Return ONLY valid JSON with no markdown formatting or additional text."""

    def parse(self, pdf_path: str, resume_id: Optional[str] = None) -> Resume:
        """
        Parse resume using pure LLM approach
        
        Args:
            pdf_path: Path to PDF resume file
            resume_id: Optional custom ID for the resume
            
        Returns:
            Resume object with all extracted data
        """
        # Extract text from PDF
        print(f"Extracting text from {pdf_path}...")
        resume_text = extract_text_from_pdf(pdf_path)
        
        if len(resume_text) < 100:
            raise ValueError("Extracted text is too short. PDF may be empty or unreadable.")
        
        print(f"Extracted {len(resume_text)} characters. Sending to LLM...")
        
        # Create prompt
        prompt = self.create_extraction_prompt(resume_text)
        
        # Call LLM
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert resume parser. Extract structured data from resumes with perfect accuracy. Return only valid JSON."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0,  # Deterministic output
                response_format={"type": "json_object"}  # Ensures valid JSON
            )
            
            # Parse response
            extracted_json = response.choices[0].message.content
            extracted_data = json.loads(extracted_json)
            
            print("✓ LLM extraction successful")
            
        except Exception as e:
            print(f"✗ LLM extraction failed: {e}")
            raise
        
        # Add resume ID
        extracted_data["id"] = resume_id or "resume_001"
        
        # Validate and create Resume object
        try:
            resume = Resume(**extracted_data)
            print("✓ Resume validation successful")
            return resume
            
        except ValidationError as e:
            print(f"✗ Validation failed: {e}")
            print(f"\nExtracted data:\n{json.dumps(extracted_data, indent=2)}")
            raise
    
    def parse_batch(self, pdf_paths: List[str]) -> List[Resume]:
        """Parse multiple resumes"""
        resumes = []
        for i, path in enumerate(pdf_paths, 1):
            print(f"\n{'='*60}")
            print(f"Processing resume {i}/{len(pdf_paths)}: {path}")
            print('='*60)
            try:
                resume = self.parse(path, resume_id=f"resume_{i:03d}")
                resumes.append(resume)
            except Exception as e:
                print(f"Failed to parse {path}: {e}")
                continue
        return resumes


# ========== Usage Example ==========
if __name__ == "__main__":
    # Initialize parser
    parser = LLMResumeParser(model="gpt-4o")
    
    # Parse resume
    resume = parser.parse(
            pdf_path="/Users/prudhvisajja/Desktop/Prudhvi_resume-BE.pdf",
            resume_id="candidate_001"
        )

    # Print results
    print("\n" + "="*60)
    print("PARSED RESUME")
    print("="*60)
    print(json.dumps(resume.model_dump(), indent=2))
