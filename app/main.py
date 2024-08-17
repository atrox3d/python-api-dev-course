from fastapi import (
    FastAPI, 
)
# from random import randrange
import logging
from sqlalchemy.orm import Session


# import schemas
try:
    from schemas import post
    # from ..schemas.post import Post
except Exception as e:
    import sys
    print(f'{sys.path=}')
    print(f'{sys.argv=}')
    print(f'{__name__=}')
    print(e)
    exit()

# sqlite
from db.sqlite import sqlite as db
from schemas.helpers.posts import default_posts
from schemas.helpers.users import default_users

# sqlalchemy
from db.orm.sqlite import (
    engine, 
    reset_db
)

from db.orm import models
from .routers.posts import router as posts_router
from .routers.users import router as users_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(posts_router)
app.include_router(users_router)

SQLALCHEMY = True
if SQLALCHEMY:
    models.Base.metadata.create_all(bind=engine)

    reset_db(
                models,
                default_posts,
                default_users,
                # drop_tables=True
             )
else:
    conn = db.setup_db('social.db', 'posts')
    db.create_db_posts(conn, default_posts)

@app.get("/")
def root() -> dict[str, str]:
    return {"message": "welcome to my api"}





