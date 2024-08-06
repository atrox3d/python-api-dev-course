from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randrange

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    id: int = None

class Posts(BaseModel):
    posts: list[Post] = []
    # count: int = 0

    def add(self, post:Post):
        self.posts.append(post)
        # self.count = len(self.posts)

posts = Posts()

app = FastAPI()

# posts = []

@app.get("/")
def root():
    return {"message": "welcome to my api"}

@app.get('/posts')
def get_posts() -> dict: 
    return {'data': posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post) -> dict:
    post.id = randrange(0, 1000000)
    print(f'{post = }')
    posts.add(post)
    return {'data': post}

def find_post(id:int) -> Post|None:
    for post in posts.posts:
        if post.id == id:
            return post

@app.get('/posts/{id}')
def get_post(
                id:int, 
                # response: Response
    ) -> Post|dict:
    if (post := find_post(id)) is not None:
        return post
    else:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'data': f'id {id} not found'}
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'id {id} not found')
    