from turtle import up
from typing import Optional
# from fastapi import Body, FastAPI, HTTPException, Response, status
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randrange
from datetime import datetime as dt
from sqlite3 import Connection, Cursor

from db import db

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    created_at: str
    id: int = None

class Posts(BaseModel):
    posts: list[Post] = []
    # count: int = 0

    def add(self, post:Post):
        self.posts.append(post)
        # self.count = len(self.posts)

def create_posts(conn:Connection, posts:Posts):
    for post in posts.posts:
        db.execute_sql(conn, '''
            INSERT INTO posts
            (title, content, published, created_at)
            VALUES
            (:title, :content, :published, :created_at)
        ''', **post.model_dump())

posts = Posts(posts=[
    Post(title='defaul post 1', content='default content 1', id=1, 
         created_at=dt.today().strftime('%Y-%m-%d %H:%M:%S')),
    Post(title='defaul post 2', content='default content 2', id=2,
         created_at=dt.today().strftime('%Y-%m-%d %H:%M:%S')),
])


conn = db.setup_db('social.db', 'posts')
create_posts(conn, posts)

app = FastAPI()

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

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    if (post := find_post(id)) is not None:
        posts.posts.remove(post)
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'id {id} not found')

@app.put('/posts/{id}')
def update_post(id:int, update:Post):
    if (post := find_post(id)) is not None:
        post.title = update.title
        post.content = update.content
        return {'updated': post}
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'id {id} not found')
    