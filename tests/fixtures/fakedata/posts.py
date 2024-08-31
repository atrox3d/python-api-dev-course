import pytest
import logging
from sqlalchemy.orm import Session

from schemas import post
from db.orm import models
import schemas.post
import schemas.user

logger = logging.getLogger(__name__)

@pytest.fixture
def fake_posts() -> list[post.PostCreate]:
    logger.debug('returning fake PostCreate list')
    return [
        post.PostCreate(title='1st title', content='1st content'),
        post.PostCreate(title='2nd title', content='2nd content'),
        post.PostCreate(title='3rd title', content='3rd content'),
    ]

@pytest.fixture
def fake_post_models_db_userid1(
    fake_posts          :list[schemas.post.PostCreate], 
    add_user_db_id1     :schemas.user.UserDb
) -> list[models.Post]:
    logger.debug('returning fake Post model list')
    return [models.Post(**_post.model_dump(), owner_id=add_user_db_id1.id) 
            for _post in fake_posts]

@pytest.fixture
def add_fake_posts_db_userid1(
        session                         :Session, 
        fake_post_models_db_userid1     :list[models.Post]
) -> list[models.Post]:
    logger.debug('saving fake posts to db')
    session.add_all(fake_post_models_db_userid1)
    session.commit()
    return session.query(models.Post).all()

@pytest.fixture
def fake_post_models_db_multiple_users(
    fake_posts      :list[schemas.post.PostCreate], 
    add_users_db    :schemas.user.UserDb
) -> list[models.Post]:
    logger.debug('returning fake Post model list')
    userids = [user.id for user in add_users_db]
    logger.info(f'----- {userids = } -------')
    return [models.Post(**_post.model_dump(), 
            owner_id=id) 
            for _post, id in zip(fake_posts, userids)]

@pytest.fixture
def add_fake_posts_db_multiple_users(
    session                             :Session, 
    fake_post_models_db_multiple_users  :list[models.Post]
) -> list[models.Post]:
    logger.debug('saving fake posts to db')
    session.add_all(fake_post_models_db_multiple_users)
    session.commit()
    return session.query(models.Post).all()
