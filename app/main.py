from fastapi import FastAPI, HTTPException, Response, status
from random import randrange

from db import sqlite
from models.post import Post, Posts
from helpers.posts import create_db_posts, get_db_posts, posts

conn = sqlite.setup_db('social.db', 'posts')
create_db_posts(conn, posts)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "welcome to my api"}

@app.get('/posts')
def get_posts() -> Posts: 
    return get_db_posts(conn)

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
    