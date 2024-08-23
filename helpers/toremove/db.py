import json
from types import ModuleType
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel

from db.orm.sqlite import SessionLocal, get_db
from db.orm import models
import schemas.post
import schemas.user
import app.utils

def reset_db(
                engine,
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

