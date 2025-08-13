from pydantic import BaseModel, EmailStr, HttpUrl
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import datetime
from typing import List




class UserBase(BaseModel):
    email: EmailStr
    password: str
    created_at: datetime = Field(default_factory=datetime.now)


class UserInsertStudent(UserBase):
    role: str = "student"



class UserInsertProfessor(UserBase):
    role: str = "professor"