from fastapi import FastAPI
import logging

# sqlite
from db.sqlite import sqlite as db
# from schemas.helpers.posts import default_posts
# from schemas.helpers.users import default_users
import schemas

# sqlalchemy
from db.orm.sqlite import engine, reset_db
from db.orm import models
# import schemas.helpers
import schemas.helpers.posts
import schemas.helpers.users
from .routers import posts
from .routers import users
from .routers import auth



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

SQLALCHEMY = True
if SQLALCHEMY:
    models.Base.metadata.create_all(bind=engine)

    reset_db(
                models,
                schemas.helpers.posts.default_posts,
                schemas.helpers.users.default_users,
                # drop_tables=True
             )
else:
    conn = db.setup_db('social.db', 'posts')
    db.create_db_posts(conn, schemas.helpers.posts.default_posts)

@app.get("/")
def root() -> dict[str, str]:
    return {"message": "welcome to my api"}





