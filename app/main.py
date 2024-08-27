from contextlib import asynccontextmanager
from operator import setitem

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from helpers.toremove.db import reset_db
import helpers.db
# import schemas

from db.orm.sqlite import engine, get_db
from db.orm import models

# import helpers.toremove.default_posts
# import helpers.default_users

from .routers import posts
from .routers import users
from .routers import auth
from .routers import vote
from .routers import example
from .routers import utility


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_db(max_votes:int=10):
    helpers.db.setup_db(
                next(get_db()),
                models,
                # delete_existing=True
                max_votes=max_votes
    )

@asynccontextmanager
async def lifespan(app:FastAPI):
    ''' enable/disable switches from .lifespan.env property file'''

    from app.config import LifespanSettings
    settings = LifespanSettings()
    print(f'LIFESPAN| start {settings=}')

    if settings.reset_db:
        #
        # this will delete all tables and recreate example data
        #
        print(f'LIFESPAN| reset_db({settings.max_votes=})')
        if settings.max_votes is not None:
            setup_db(settings.max_votes)    # specify max generated votes
        else:
            setup_db()                      # use default max votes
    else:
        if settings.import_users and settings.json_users:
            #
            # this will import users from json and optionally delete previews users
            # of course if we import the same users this will violate integrity
            #
            if settings.delete_users:
                #
                # this will delete users table and related posts cascade
                #
                print(f'LIFESPAN| delete users')
                helpers.db.delete_all_records(
                    next(get_db()),
                    models.User
                )
            print(f'LIFESPAN| import users')
            helpers.db.import_users(
                next(get_db()),
                filename=settings.json_users,
                max_rows=settings.max_users
            )

        if settings.import_posts and settings.json_posts:
            #
            # this will import posts from json and optionally delete previews posts
            #
            if settings.delete_posts:
                #
                # this will delete existing posts
                #
                print(f'LIFESPAN| delete posts')
                helpers.db.delete_all_records(
                    next(get_db()),
                    models.Post
                )
            print(f'LIFESPAN| import posts')
            helpers.db.import_posts(
                next(get_db()),
                filename=settings.json_posts,
                max_rows=settings.max_posts
            )
        
        if settings.fake_votes and settings.max_votes:
            #
            # this will randomly create likes to posts
            # any integrity violation is ignored
            #
            print(f'LIFESPAN| delete votes')
            helpers.db.delete_all_records(
                next(get_db()),
                models.Vote
            )
            print(f'LIFESPAN| create votes')
            helpers.db.create_votes(
                next(get_db()),
                models,
                settings.max_votes
            )
    
    yield
    print(f'LIFESPAN| end {settings=}')


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(example.router)
app.include_router(utility.router)

# create db if not existing
# models.Base.metadata.create_all(bind=engine)

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





