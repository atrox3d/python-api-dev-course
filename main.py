from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
from random import randint

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    id: int = None

class Posts(BaseModel):
    posts: list = []
    count: int = 0

app = FastAPI()

posts = []

@app.get("/")
def root():
    return {"message": "welcome to my api"}

@app.get('/posts')
def get_posts():
    return {'data': 'this is your post'}

@app.post('/posts')
def create_post(post: Post) -> Posts:
    post.id = randint(1, 10000)
    print(f'{post = }')
    posts.append(post)
    return Posts(posts = posts, count=len(posts))

