import pytest
import logging

from schemas import post
from schemas import user
from schemas import vote
from db.orm import models

logger = logging.getLogger(__name__)

@pytest.fixture
def fake_posts() -> list[post.PostCreate]:
    logger.debug('returning fake PostCreate list')
    return [
        post.PostCreate(title='1st title', content='1st content'),
        post.PostCreate(title='2nd title', content='2nd content'),
        post.PostCreate(title='3rd title', content='3rd content'),
        # post.PostCreate(title='4th title', content='4th content'),
    ]

@pytest.fixture
def fake_post_models_db_userid1(fake_posts, add_user_db_id1) -> list[models.Post]:
    logger.debug('returning fake Post model list')
    return [models.Post(**_post.model_dump(), owner_id=add_user_db_id1.id) 
            for _post in fake_posts]

@pytest.fixture
def add_fake_posts_db_userid1(session, fake_post_models_db_userid1) -> list[models.Post]:
    logger.debug('saving fake posts to db')
    session.add_all(fake_post_models_db_userid1)
    session.commit()
    return session.query(models.Post).all()

@pytest.fixture
def fake_post_models_db_multiple_users(fake_posts, add_users_db) -> list[models.Post]:
    logger.debug('returning fake Post model list')
    userids = [user.id for user in add_users_db]
    logger.info(f'----- {userids = } -------')
    return [models.Post(**_post.model_dump(), 
            owner_id=id) 
            for _post, id in zip(fake_posts, userids)]

@pytest.fixture
def add_fake_posts_db_multiple_users(session, fake_post_models_db_multiple_users) -> list[models.Post]:
    logger.debug('saving fake posts to db')
    session.add_all(fake_post_models_db_multiple_users)
    session.commit()
    return session.query(models.Post).all()
