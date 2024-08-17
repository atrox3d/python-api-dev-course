from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
import logging

from app import utils
# sqlite
from db.sqlite import sqlite as db
import schemas

# sqlalchemy
from db.orm.sqlite import get_db
from db.orm import models

router = APIRouter(prefix='/users', tags=['Users'])

@router.post('/', 
          status_code=status.HTTP_201_CREATED,
          response_model=schemas.user.UserOut
)
def create_user(
                    user: schemas.user.UserCreate, 
                    db: Session = Depends(get_db)
# ):
) -> schemas.user.UserOut:
    user.password = utils.hash(user.password)

    new_user = models.User(
        **user.model_dump()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get(
            '/{id}',
            response_model=schemas.user.UserOut
)
def get_user(
                id: int,
                db: Session = Depends(get_db)
):
    print(f'{id=}')
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User {id=} not found')
    return user
