import pytest
import logging

from schemas import post
from schemas import user
from schemas import vote
from db.orm import models
import app.oauth2
import schemas.vote

logger = logging.getLogger(__name__)

def test_authorized_vote(session, authorized_client, token, add_fake_posts_db_multiple_users):
    tokendata = app.oauth2.verify_access_token(token, app.oauth2.unhautorized_exception)
    
    for post in add_fake_posts_db_multiple_users:
        if post.owner_id != tokendata.id:
            break
    post_id = post.id
    owner_id = post.owner_id
    vote = schemas.vote.Vote(post_id=post_id, dir=1)
    response = authorized_client.post(
                        '/vote',
                        json=vote.model_dump()
    )
    assert response.status_code == 201
    votedb: models.Vote = (
                session.query(models.Vote)
                .filter(
                    models.Vote.post_id==post_id, 
                    models.Vote.user_id==tokendata.id
                )
              .first()
    )
    assert votedb.post_id == vote.post_id
    assert votedb.post_id == owner_id


