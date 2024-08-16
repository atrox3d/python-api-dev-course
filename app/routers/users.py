from typing_extensions import deprecated
from fastapi import (
    FastAPI, HTTPException, Response, status, Depends, APIRouter
)
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

router = APIRouter()

@router.post('/users', 
          status_code=status.HTTP_201_CREATED,
          response_model=schemas.UserOut
)
def create_user(
                    user: schemas.UserCreate, 
                    db: Session = Depends(get_db)
# ):
) -> schemas.UserOut:
    user.password = utils.hash(user.password)

    new_user = models.User(
        **user.model_dump()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get(
            '/users/{id}',
            response_model=schemas.UserOut
)
def get_user(
                id: int,
                db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User {id=} not found')
    return user
