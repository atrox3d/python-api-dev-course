from pydantic import BaseModel, EmailStr
from datetime import datetime as dt

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: dt

class UserDb(UserOut):
    password: str

Users = list[UserCreate]

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None
