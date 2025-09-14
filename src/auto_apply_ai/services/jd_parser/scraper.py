import os
import requests
from bs4 import BeautifulSoup
import json
from html import unescape
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import sys
import asyncio
from pathlib import Path
from playwright.sync_api import sync_playwright
try:
    from .schemas import JobDesc
except Exception:
    # Allow running this file directly as a script
    sys.path.append(str(Path(__file__).resolve().parents[3] / "src"))
    from auto_apply_ai.services.jd_parser.schemas import JobDesc
from typing import Optional



def open_browser():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    return p, browser, context


def open_page(context, url: str):
    page = context.new_page()
    page.goto(url, wait_until="networkidle", timeout=60000)
    return page
    



def parse_jd_with_llm(content: str, api_key: str, model: str = "gemini-2.0-flash-lite") -> Optional[JobDesc]:
    """
    Parse job description HTML content using an LLM to extract structured data.
    
    Args:
        content: Accessibility (AX) tree snapshot (e.g., from Playwright's page.accessibility.snapshot())
        api_key: Google Generative AI API key
        model: Gemini model to use (default: gemini-2.0-flash-lite)
    
    Returns:
        JobDesc object with structured data or None if parsing fails
    """
    if not content:
        return None
    
    try:
        # Initialize the LLM (Gemini)
        llm = ChatGoogleGenerativeAI(
            api_key=api_key,
            model=model,
            temperature=0
        )
        
        # Create the prompt template
        prompt = ChatPromptTemplate.from_template("""
        You are an expert at parsing job descriptions from accessibility (AX) trees.
        The input is an accessibility snapshot representing the structure and text content of a job page. It consists of roles, names, values, and children rather than raw HTML.
        
        AX Tree Input:
        {ax_content}
        
        Extract the following fields for the JobDesc schema and return **valid JSON**:
        - role: Job title/role
        - company: Company name
        - location: Job location
        - employment_type: Employment type (e.g., Full-time, Part-time, Contract)
        - must_have: List of required skills/qualifications
        - nice_to_have: List of preferred skills/qualifications
        - responsibilities: List of job responsibilities
        - tools: List of tools/technologies mentioned
        - keywords: List of relevant keywords from the job description
        - years_experience: Experience requirements as a dict
        - salary: Salary information if available (min, max, currency)
        - meta: Any additional metadata as a dictionary
        
        Notes:
        - Use headings/landmarks/roles (e.g., heading/name, list, listitem, paragraph) to infer sections like Responsibilities or Requirements.
        - If a field is unavailable, use null or an empty list/string appropriately.
        - Respond with a JSON object that conforms to the JobDesc pydantic schema.
        """)
        
        # Create the output parser
        output_parser = JsonOutputParser(pydantic_object=JobDesc)
        
        # Create the chain
        chain = prompt | llm | output_parser
        
        # Run the chain
        result = chain.invoke({"ax_content": content})
        
        return result
        
    except Exception as e:
        print(f"Error parsing JD with LLM: {e}")
        return None



def fetch_and_parse_job(url: str, api_key: Optional[str] = None, model: str = "gemini-2.0-flash-lite") -> Optional[JobDesc]:
    """
    High-level orchestration: given a job posting URL, launch a headless browser,
    capture the page accessibility (AX) snapshot, and parse it into a JobDesc via LLM.

    Args:
        url: Job description URL
        api_key: Google Generative AI API key. If None, falls back to GEMINI_KEY env var.
        model: Gemini model name

    Returns:
        JobDesc instance or None on failure.
    """
    if not api_key:
        api_key = os.getenv("GEMINI_KEY")

    p = browser = context = None
    try:
        p, browser, context = open_browser()
        page = open_page(context, url)
        ax = page.accessibility.snapshot()
        return parse_jd_with_llm(ax, api_key=api_key, model=model)
    except Exception as e:
        print(f"Error in fetch_and_parse_job: {e}")
        return None
    finally:
        try:
            if browser:
                browser.close()
        finally:
            if p:
                p.stop()


if __name__ == "__main__":
    demo_url = "https://transunion.wd5.myworkdayjobs.com/en-GB/TransUnion/job/Alderley-Edge/Senior-Systems-Developer_19035213"
    # Example usage:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GEMINI_KEY")
    job = fetch_and_parse_job(demo_url, api_key=api_key)
    print(json.dumps(job, indent=1))