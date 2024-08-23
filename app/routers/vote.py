from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
import logging

from app import oauth2, utils
# sqlite
# from db.sqlite import sqlite as db
import schemas.vote

# sqlalchemy
from db.orm.sqlite import get_db
from db.orm import models

router = APIRouter(prefix='/vote', tags=['vote'])

@router.post('/', 
          status_code=status.HTTP_201_CREATED,
        #   response_model=schemas.user.UserOut
)
def vote(
            vote: schemas.vote.Vote, 
            db: Session = Depends(get_db),
            current_user: models.User = Depends(oauth2.get_current_user),
):
    
    if not (db.query(models.Post)
            .filter(models.Post.id==vote.post_id)
            .first()):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='post not found'
        )

    vote_query = (
                db.query(models.Vote)
                .filter(
                        models.Vote.post_id==vote.post_id,
                        models.Vote.user_id==current_user.id
                )
    )
    found_vote:models.Vote = vote_query.first()
    print(vote)

    if vote.dir == 1:
        if found_vote is not None:
            print(found_vote.post_id)
            print(found_vote.user_id)
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='already voted')
        else:
            print('not voted')
            db.add(models.Vote(post_id=vote.post_id, 
                            user_id=current_user.id))
            db.commit()
            return {'message': 'successfully liked'}
    else:
        if found_vote is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='vote does not exist')
        else:
            vote_query.delete()
            db.commit()
            return {'message': 'successfully unliked'}
    
