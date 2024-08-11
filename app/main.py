from re import L
from fastapi import FastAPI, HTTPException, Response, status
from random import randrange
import logging

from db import sqlite as db
from models.post import Post, Posts
# from db.sqlite import create_db_posts, get_db_posts
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

# def find_post(id:int) -> Post|None:
#     for post in default_posts.posts:
#         if post.id == id:
#             return post

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
    # if (post := find_post(id)) is not None:
    if db.find_db_post(conn, id):
        db.delete_db_post(conn, id)
    #     default_posts.posts.remove(post)
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
    