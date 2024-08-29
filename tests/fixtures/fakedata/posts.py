import pytest

from schemas import post
from schemas import user
from schemas import vote
from db.orm import models

@pytest.fixture
def fake_posts() -> list[post.PostCreate]:
    return [
        post.PostCreate(title='1st title', content='1st content'),
        post.PostCreate(title='2st title', content='1st content'),
        post.PostCreate(title='3st title', content='1st content'),
    ]

@pytest.fixture
def fake_post_models_db(fake_posts, add_user_db) -> list[models.Post]:
    return [models.Post(**_post.model_dump(), owner_id=add_user_db.id) 
            for _post in fake_posts]

@pytest.fixture
def add_fake_posts_db(session, fake_post_models_db) -> list[models.Post]:
    session.add_all(fake_post_models_db)
    session.commit()
    return session.query(models.Post).all()
