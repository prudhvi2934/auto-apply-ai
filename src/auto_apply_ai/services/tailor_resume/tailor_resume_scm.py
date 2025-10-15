from re import S
from typing import List, Optional
from pydantic import BaseModel

class Basics(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None


class Experience(BaseModel):
    id: str
    company: str
    title: str
    start: str
    end: str
    bullet_point: List[str]


class Resume(BaseModel):
    id: str
    basics: Basics 
    summary: str
    skills: List[str] 
    experience: List[Experience] = []
    education: str
    certifications: Optional[str] = None
    projects: Optional[str] = None

