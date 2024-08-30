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
        post.PostCreate(title='2st title', content='1st content'),
        post.PostCreate(title='3st title', content='1st content'),
    ]

@pytest.fixture
def fake_post_models_db(fake_posts, add_user_db) -> list[models.Post]:
    logger.debug('returning fake Post model list')
    return [models.Post(**_post.model_dump(), owner_id=add_user_db.id) 
            for _post in fake_posts]

@pytest.fixture
def add_fake_posts_db(session, fake_post_models_db) -> list[models.Post]:
    logger.debug('saving fake posts to db')
    session.add_all(fake_post_models_db)
    session.commit()
    return session.query(models.Post).all()
