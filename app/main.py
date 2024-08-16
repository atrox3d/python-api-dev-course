from typing_extensions import deprecated
from fastapi import FastAPI, HTTPException, Response, status, Depends
from random import randrange
import logging
from sqlalchemy.orm import Session

import utils
# sqlite
from db import sqlite as db
# from schemas.post import Post, Posts
import schemas
from helpers.posts import default_posts
from helpers.users import default_users

# sqlalchemy
from orm.sqlite import (
    engine, SessionLocal, Base, get_db, reset_db
)

from orm import models
from .routers.posts import router as posts_router
from .routers.users import router as users_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SQLALCHEMY = True

app = FastAPI()
app.include_router(posts_router)
app.include_router(users_router)


if SQLALCHEMY:
    models.Base.metadata.create_all(bind=engine)

    reset_db(
                models,
                default_posts,
                default_users,
                #  True
             )
    
    @app .get('/sqlalchemy')
    def test_sql_alchemy(db: Session = Depends(get_db)) -> dict[str, str|schemas.Posts]:
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





