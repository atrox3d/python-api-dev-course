from fastapi import FastAPI, HTTPException, Response, status, Depends
from random import randrange
import logging

from sqlalchemy.orm import Session

# sqlite
from db import sqlite as db
from models.post import Post, Posts
from helpers.posts import default_posts

# sqlalchemy
from orm.sqlite import engine, SessionLocal, Base, get_db
from orm import models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SQLALCHEMY = True

app = FastAPI()

if SQLALCHEMY:
    models.Base.metadata.create_all(bind=engine)

    @app .get('/sqlalchemy')
    def test_sql_alchemy(db: Session = Depends(get_db)):
        query = db.query(models.Post)
        print(query)
        posts = query.all()
        return {'query': str(query), 'data': posts}
    
else:
    conn = db.setup_db('social.db', 'posts')
    db.create_db_posts(conn, default_posts)

@app.get("/")
def root():
    return {"message": "welcome to my api"}

@app.get('/posts')
def get_posts(db: Session = Depends(get_db)): 
    # return db.get_db_posts(conn)
    return db.query(models.Post).all()

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
