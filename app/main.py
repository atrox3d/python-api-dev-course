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

    _db = SessionLocal()
    print('MAIN| deleting all  posts')
    _db.query(models.Post).delete()
    for post in default_posts:
        print(f'MAIN| adding {post}')
        new_post = models.Post(**post.model_dump())
        _db.add(new_post)
        _db.commit()
    _db.close()
    
    @app .get('/sqlalchemy')
    def test_sql_alchemy(db: Session = Depends(get_db)) -> dict[str, str|Posts]:
        query = db.query(models.Post)
        print(query)
        posts = query.all()
        return {'query': str(query), 'data': posts}
    
else:
    conn = db.setup_db('social.db', 'posts')
    db.create_db_posts(conn, default_posts)

@app.get("/")
def root() -> dict[str, str]:
    return {"message": "welcome to my api"}

@app.get('/posts')
def get_posts(db: Session = Depends(get_db)) -> Posts:   # -> ????
    # return db.get_db_posts(conn)
    return db.query(models.Post).all()

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)) -> dict[str, Post]:
    # db.create_db_post(conn, post)
    new_post = models.Post(
        **post.model_dump()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {'data': new_post}

@app.get('/posts/{id}')
def get_post(
                id:int, 
                # response: Response
                db: Session = Depends(get_db)
    ) -> Post:
    # post = db.find_db_post(conn, id)
    print('retrieving post')
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if post:
        return post
    else:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'data': f'id {id} not found'}
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'id {id} not found')

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):

    # if db.find_db_post(conn, id):
        # db.delete_db_post(conn, id)
    query = db.query(models.Post).filter(models.Post.id == id)
    if query.first():
        query.delete()
        db.commit()
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'id {id} not found')

@app.put('/posts/{id}')
def update_post(id:int, update:Post, db: Session = Depends(get_db)) -> dict[str, Post]:
    # post = db.find_db_post(conn, id)
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if post:
        post.title = update.title
        post.content = update.content
        # db.update_db_post(conn, id, post.model_dump())
        print(update.model_dump())
        query.update(
                update.model_dump()
                # {'title': 'updated', 'content': 'updated'}
            )
        db.commit()
        db.refresh(post)
        return {'updated': post}
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'id {id} not found')
