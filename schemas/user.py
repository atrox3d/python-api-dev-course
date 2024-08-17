from pydantic import BaseModel, EmailStr
from datetime import datetime as dt

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: dt

Users = list[UserCreate]