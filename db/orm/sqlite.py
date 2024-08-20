# https://fastapi.tiangolo.com/tutorial/sql-databases

from types import ModuleType
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import schemas.post
import schemas.user

import app.utils

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
############################ß######################################


SQLALCHEMY_DATABASE_URL = "sqlite:///social.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
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
        print('MAIN| dropping table posts')
        models.User.__table__.drop(engine)
        models.Post.__table__.drop(engine)
        print('MAIN| dropping table users')
        models.User.__table__.create(engine)
        models.Post.__table__.create(engine)
        _db.commit()

    print('MAIN| deleting all users')
    _db.query(models.User).delete()
    if create_users:
        for user in create_users:
            print(f'MAIN| adding {user}')
            user.password = app.utils.hash(user.password)
            new_user = models.User(**user.model_dump())
            _db.add(new_user)
            _db.commit()


    print('MAIN| deleting all posts')
    _db.query(models.Post).delete()
    if create_posts:
        for post in create_posts:
            print(f'MAIN| adding {post}')
            new_post = models.Post(**post.model_dump())
            _db.add(new_post)
            _db.commit()

    _db.close()
