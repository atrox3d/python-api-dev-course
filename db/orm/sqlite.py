# https://fastapi.tiangolo.com/tutorial/sql-databases

from types import ModuleType
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import schemas.post
import schemas.user

import app.utils
from config import sqlite_settings

##################################################################
# ENFORCE SQLITE FOREIGN KEY
# https://stackoverflow.com/a/77708922
##################################################################
from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
##################################################################


# SQLALCHEMY_DATABASE_URL = "sqlite:///social.db"
SQLALCHEMY_DATABASE_URL = sqlite_settings.database_url
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def reset_db(
                models:ModuleType, 
                create_posts:schemas.post.Posts=None,
                create_users:schemas.user.Users=None,
                drop_tables:bool=False
):
    _db = SessionLocal()

    if drop_tables:
        print('RESET_DB| dropping table votes')
        models.Vote.__table__.drop(engine)

        print('RESET_DB| dropping table users')
        models.User.__table__.drop(engine)

        print('RESET_DB| dropping table posts')
        models.Post.__table__.drop(engine)



        print('RESET_DB| creating table users')
        models.User.__table__.create(engine)

        print('RESET_DB| creating table posts')
        models.Post.__table__.create(engine)

        print('RESET_DB| creating table votes')
        models.Vote.__table__.create(engine)
    _db.commit()

    print('RESET_DB| deleting all users')
    _db.query(models.User).delete()
    if create_users:
        for user in create_users:
            print(f'RESET_DB| adding {user}')
            user.password = app.utils.hash(user.password)
            new_user = models.User(**user.model_dump())
            _db.add(new_user)
    _db.commit()


    print('RESET_DB| deleting all posts')
    _db.query(models.Post).delete()
    if create_posts:
        for post in create_posts:
            print(f'RESET_DB| adding {post}')
            new_post = models.Post(**post.model_dump())
            _db.add(new_post)
            _db.commit()


    print('RESET_DB| deleting all votes, if any')
    _db.query(models.Vote).delete()
    print(f'RESET_DB| adding vote')
    _db.add(models.Vote(post_id=1, user_id=2))
    _db.commit()


    _db.close()
