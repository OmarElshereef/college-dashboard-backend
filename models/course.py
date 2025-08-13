from pydantic import BaseModel, EmailStr, HttpUrl
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import datetime
from typing import List




class CourseCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    professor_id: int
    max_students: int = 50
    current_enrollment: int = 0

class Course(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str]
    professor_id: int
    max_students: int
    current_enrollment: int
    created_at: datetime
