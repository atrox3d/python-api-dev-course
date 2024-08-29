import pytest

from schemas import post
from schemas import user
from schemas import vote
from db.orm import models

@pytest.fixture
def fake_create_posts() -> list[post.PostCreate]:
    return [
        post.PostCreate(title='1st title', content='1st content'),
        post.PostCreate(title='2st title', content='1st content'),
        post.PostCreate(title='3st title', content='1st content'),
    ]

@pytest.fixture
def fake_models_post(fake_create_posts, new_user) -> list[models.Post]:
    return [models.Post(**_post.model_dump(), owner_id=new_user.id) 
            for _post in fake_create_posts]

