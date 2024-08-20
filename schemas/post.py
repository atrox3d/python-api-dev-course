from pydantic import BaseModel
from datetime import datetime as dt

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    user_id: int

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
