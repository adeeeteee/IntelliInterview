from pydantic import BaseModel
from typing import List


class Project(BaseModel):
    name: str
    technologies: List[str] = []
    description: str = ""


class ResumeData(BaseModel):
    name: str
    email: str = ""
    education: List[str] = []
    skills: List[str] = []
    projects: List[Project] = []
    experience: List[str] = []
    certifications: List[str] = []