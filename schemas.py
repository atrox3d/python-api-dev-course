from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime as dt

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    # rating: Optional[int] = None
    # created_at: str = Field(default_factory=lambda:dt.today().strftime('%Y-%m-%d %H:%M:%S'))
    # created_at: dt = Field(default_factory=lambda:dt.today())
    # created_at: dt
    # id: int = None

class PostCreate(PostBase): pass

class Post(PostBase):
    id: int
    created_at: dt

    # class Config:
        # orm_mode = True

Posts = list[Post]

class User(BaseModel):
    email: str
    password: str

Users = list[User]