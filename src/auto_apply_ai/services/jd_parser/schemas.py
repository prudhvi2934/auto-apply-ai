from typing import List, Optional, Dict
from pydantic import BaseModel

class Salary(BaseModel):
    min: Optional[float]
    max: Optional[float]
    currency: Optional[str]

class JobDesc(BaseModel):
    role: Optional[str]
    company: Optional[str]
    location: Optional[str]
    employment_type: Optional[str]
    must_have: List[str] = []
    nice_to_have: List[str] = []
    responsibilities: List[str] = []
    tools: List[str] = []
    keywords: List[str] = []
    years_experience: Optional[Dict[str, int]] = None
    salary: Optional[Salary] = None
    meta: Dict = {}