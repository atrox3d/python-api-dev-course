from contextlib import asynccontextmanager

from fastapi import FastAPI
import logging

from helpers.toremove.db import reset_db
import helpers.db
import schemas

from db.orm.sqlite import engine, get_db
from db.orm import models

import helpers.toremove.default_posts
import helpers.default_users

from .routers import posts
from .routers import users
from .routers import auth
from .routers import vote
from .routers import example
from .routers import utility


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app:FastAPI):
    from config import LifespanSettings
    settings = LifespanSettings()
    print(f'LIFESPAN| start {settings=}')
    yield
    print(f'LIFESPAN| end {settings=}')

app = FastAPI(lifespan=lifespan)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(example.router)
app.include_router(utility.router)

# create db if not existing
models.Base.metadata.create_all(bind=engine)

if False:
    helpers.db.setup_db(
                next(get_db()),
                models,
                # delete_existing=True
                max_votes=10
    )

##########################################################
# test PRAGMA foreign_keys, on delete cascade
# _db = next(get_db())

# for row in _db.query(models.Post).all():
#     print(row)
# _db.query(models.User).delete()
# _db.commit()
# for row in _db.query(models.Post).all():
#     print(row)
##########################################################

@app.get("/")
def root() -> dict[str, str]:
    return {"message": "welcome to my api"}





