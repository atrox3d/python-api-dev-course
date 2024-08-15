from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime as dt

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None
    # created_at: str = Field(default_factory=lambda:dt.today().strftime('%Y-%m-%d %H:%M:%S'))
    created_at: dt = Field(default_factory=lambda:dt.today())
    # created_at: dt
    # id: int = None


class Posts(BaseModel):
    posts: list[Post] = []
    # count: int = 0

    def add(self, post:Post):
        self.posts.append(post)
        # self.count = len(self.posts)
