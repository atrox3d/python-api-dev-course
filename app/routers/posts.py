from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
import logging

# sqlite
from db.sqlite import sqlite as db
import schemas.post

# sqlalchemy
from db.orm.sqlite import get_db
from db.orm import models

from app import oauth2

router = APIRouter(prefix='/posts', tags=['Posts'])

@router.get(
        '/',
         response_model=schemas.post.Posts
)
def get_posts(
                db: Session = Depends(get_db)
) -> schemas.post.Posts:
    # return db.get_db_posts(conn)
    return db.query(models.Post).all()

@router.get(
        '/owned',
         response_model=schemas.post.Posts,
)
def get_owned_posts(
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)
) -> schemas.post.Posts:
    # return db.get_db_posts(conn)
    # return db.query(models.Post).all()
    return db.query(models.Post).filter(models.Post.owner_id==current_user.id)

@router.post('/',
          status_code=status.HTTP_201_CREATED,
          response_model=schemas.post.Post
)
def create_post(
                    post: schemas.post.PostCreate, 
                    db: Session = Depends(get_db),
                    current_user: models.User = Depends(oauth2.get_current_user)
):
# ) -> schemas.post.Post:
    # db.create_db_post(conn, post)
    print(f'CREATE_POST| {current_user = }')
    print(f'CREATE_POST| { {c.name: getattr(current_user, c.name) for c in current_user.__table__.columns} }')
    new_post = models.Post(
        **post.model_dump(),
        owner_id=current_user.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get(
          '/{id}',
          response_model=schemas.post.Post
)
def get_post(
                id:int, 
                # response: Response
                db: Session = Depends(get_db)
) -> schemas.post.Post:
    # post = db.find_db_post(conn, id)
    print('retrieving post')
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if post:
        return post
    else:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'data': f'id {id} not found'}
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'id {id} not found')

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
                    id:int, 
                    db: Session = Depends(get_db),
                    current_user: models.User = Depends(oauth2.get_current_user)
):
    # if db.find_db_post(conn, id):
        # db.delete_db_post(conn, id)
    query = db.query(models.Post).filter(models.Post.id == id)

    post: models.Post = query.first()
    if post:
        if post.owner_id == current_user.id:
            query.delete()
            db.commit()
        else:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f'not authorized to delete')
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'id {id} not found')

@router.put(
        '/{id}',
        response_model=schemas.post.Post # precedence over hint
)
def update_post(
                    id:int, 
                    update:schemas.post.PostCreate, 
                    db: Session = Depends(get_db),
                    current_user: models.User = Depends(oauth2.get_current_user)
) -> schemas.post.PostBase:
    # post = db.find_db_post(conn, id)
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if post:
        if post.owner_id == current_user.id:
            post.title = update.title
            post.content = update.content
            # db.update_db_post(conn, id, post.model_dump())
            print(update.model_dump())
            query.update(
                    update.model_dump()
                    # {'title': 'updated', 'content': 'updated'}
                )
            db.commit()
            db.refresh(post)
            return post
        else:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f'not authorized to update')
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'id {id} not found')

