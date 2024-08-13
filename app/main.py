from re import L
from fastapi import FastAPI, HTTPException, Response, status
from random import randrange
import logging

from db import sqlite as db
from models.post import Post, Posts
from helpers.posts import default_posts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

conn = db.setup_db('social.db', 'posts')
db.create_db_posts(conn, default_posts)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "welcome to my api"}

@app.get('/posts')
def get_posts() -> Posts: 
    return db.get_db_posts(conn)

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post) -> dict:
    db.create_db_post(conn, post)
    return {'data': post}

@app.get('/posts/{id}')
def get_post(
                id:int, 
                # response: Response
    ) -> Post:
    post = db.find_db_post(conn, id)
    if post:
        return post
    else:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'data': f'id {id} not found'}
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'id {id} not found')

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    if db.find_db_post(conn, id):
        db.delete_db_post(conn, id)
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'id {id} not found')

@app.put('/posts/{id}')
def update_post(id:int, update:Post):
    post = db.find_db_post(conn, id)
    if post:
        post.title = update.title
        post.content = update.content
        db.update_db_post(conn, id, post.model_dump())
        return {'updated': post}
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'id {id} not found')
