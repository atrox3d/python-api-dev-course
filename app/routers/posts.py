from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
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
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user),
                # query params:
                limit:int=10,
                skip:int=0,
                search:str=''
):
# ) -> schemas.post.Posts:
    # return db.get_db_posts(conn)
    print(f'GET_POSTS| {limit=}')
    print(f'GET_POSTS| {skip=}')
    print(f'GET_POSTS| {search=!r}')
    
    # select * from posts 
    # inner join users 
    # on posts.owner_id = users.id
    # where posts.title like '%SEARCH%'
    # limit LIMIT
    # offset SKIP
    # return (
    #         db.query(models.Post)
    #         .filter(models.Post.title.contains(search))
    #         .limit(limit)
    #         .offset(skip)
    #         .all()
    # )

    # SELECT posts.*, COUNT(votes.post_id) as votes
    # FROM posts LEFT JOIN votes
    # ON posts.id = votes.post_id
    # -- WHERE posts.id = 1
    # GROUP BY posts.id;
    query = (db.query(models.Post, func.count(models.Vote.post_id).label('votes'))
            .join(
                    models.Vote, 
                    models.Post.id==models.Vote.post_id,
                    isouter=True)
            .group_by(models.Post.id))
    # print(f'{query = !s}')
    return (
            query
            # .filter(models.Post.title.contains(search))
            # .limit(limit)
            # .offset(skip)
            .all()
    )

@router.get(
        '/owned',
         response_model=schemas.post.Posts,
)
def get_owned_posts(
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)
) -> schemas.post.Posts:
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
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)
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

