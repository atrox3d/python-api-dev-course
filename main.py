from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

app = FastAPI()


@app.get("/")
def root():
    return {"message": "welcome to my api"}

@app.get('/posts')
def get_posts():
    return {'data': 'this is your post'}

@app.post('/createpost')
def create_post(newpost: Post):
    print(f'{newpost = }')
    return {
        'received': newpost
    }