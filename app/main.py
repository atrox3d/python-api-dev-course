from fastapi import FastAPI
import logging

import schemas

# sqlalchemy
from db.orm.sqlite import engine, reset_db, get_db
from db.orm import models

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

models.Base.metadata.create_all(bind=engine)

reset_db(
            models,
            create_posts=schemas.helpers.posts.default_posts,
            # create_posts=None,
            create_users=schemas.helpers.users.default_users,
            drop_tables=True
        )

# test PRAGMA foreign_keys, on delete cascade
# _db = next(get_db())

# for row in _db.query(models.Post).all():
#     print(row)
# _db.query(models.User).delete()
# _db.commit()
# for row in _db.query(models.Post).all():
#     print(row)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "welcome to my api"}





