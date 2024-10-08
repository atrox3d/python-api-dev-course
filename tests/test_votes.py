from fastapi.testclient import TestClient
import logging

from db.orm import models
import app.oauth2
import schemas.vote

logger = logging.getLogger(__name__)

def test_authorized_vote(
        session: app.oauth2.Session, 
        authorized_client: TestClient, 
        token: str, 
        add_fake_posts_db_multiple_users: list[models.Post]
):
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

def test_unauthorized_vote(
                    unauthorized_client: TestClient, 
                    add_fake_posts_db_multiple_users: list[models.Post]
):
    post_id = add_fake_posts_db_multiple_users[0].id
    vote = schemas.vote.Vote(post_id=post_id, dir=1)
    response = unauthorized_client.post(
                        '/vote',
                        json=vote.model_dump()
    )
    assert response.status_code == 401


def test_duplicate_vote(
        session: app.oauth2.Session, 
        authorized_client: TestClient, 
        token: str, 
        add_fake_posts_db_multiple_users: list[models.Post]
):
    tokendata = app.oauth2.verify_access_token(token, app.oauth2.unhautorized_exception)
    
    for post in add_fake_posts_db_multiple_users:
        if post.owner_id != tokendata.id:
            break
    post_id = post.id
    vote = schemas.vote.Vote(post_id=post_id, dir=1)
    response = authorized_client.post(
                        '/vote',
                        json=vote.model_dump()
    )
    assert response.status_code == 201
    response = authorized_client.post(
                        '/vote',
                        json=vote.model_dump()
    )
    assert response.status_code == 409

