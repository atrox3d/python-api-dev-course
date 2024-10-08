from pydantic import BaseModel
from datetime import datetime as dt

from . import user

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

class PostDefault(PostBase):
    owner_id:int

class Post(PostBase):
    id: int
    created_at: dt
    owner_id:int

    # class Config:
        # orm_mode = True
    owner: user.UserOut

class PostOut(BaseModel):
    Post: Post
    votes: int

Posts = list[PostOut]
