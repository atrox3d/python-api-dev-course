import email
import json
import pytest
import logging

# from app.routers import posts
from app.routers import auth
import app.oauth2
from db.orm import models
import tests.debug
import schemas.post

logger = logging.getLogger(__name__)

def  setup_module():
    tests.debug.DEBUG = False

def test_get_all_posts(authorized_client, add_fake_posts_db_userid1):
    response = authorized_client.get('/posts')
    assert response.status_code == 200
    # posts = [schemas.post.PostOut(**post) for post in response.json()]
    # [print(post) for post in posts]
    # posts = response.json()
    print(json.dumps(response.json(), indent=2))
    posts = [schemas.post.Post(**post.get('Post')) for post in response.json()]
    assert len(posts) == len(add_fake_posts_db_userid1)
    for post, dbpost in zip(posts, add_fake_posts_db_userid1):
        assert post.id == dbpost.id
        assert post.title == dbpost.title
        assert post.content == dbpost.content
        assert post.published == dbpost.published
        assert post.created_at == dbpost.created_at
        assert post.owner_id == dbpost.owner_id

def test_unauthorized_get_all_posts(unauthorized_client, add_fake_posts_db_userid1):
    response = unauthorized_client.get('/posts')
    assert response.status_code == 401

def test_unauthorized_get_one_post(unauthorized_client, add_fake_posts_db_userid1):
    response = unauthorized_client.get(f'/posts/{add_fake_posts_db_userid1[0].id}')
    assert response.status_code == 401

def test_get_one_posts_not_exist(authorized_client, add_fake_posts_db_userid1):
    response = authorized_client.get(
        f'/posts/-1')
    assert response.status_code == 404

def test_get_one_post(authorized_client, add_fake_posts_db_userid1):
    response = authorized_client.get(f'/posts/{add_fake_posts_db_userid1[0].id}')
    assert response.status_code == 200
    post = schemas.post.Post(**response.json())
    assert post.id == add_fake_posts_db_userid1[0].id

@pytest.mark.parametrize(
        'title, content, published',
        [
            ('new title', 'new content', True),
            ('new second title', 'new second content', False),
            ('new third title', 'new third content', True),
        ]
)
def test_create_post(
                    authorized_client,
                    add_user_db_id1,
                    add_fake_posts_db_userid1,
                    title,
                    content,
                    published
):
    response = authorized_client.post(
                'posts',
                json=dict(
                    title=title,
                    content=content,
                    published=published
                )
    )
    assert response.status_code == 201
    post = schemas.post.Post(**response.json())
    assert post.title == title
    assert post.content == content
    assert post.published == published
    assert post.owner_id == add_user_db_id1.id
    assert post.owner.email == add_user_db_id1.email

@pytest.mark.parametrize(
        'title, content',
        [
            ('new title', 'new content'),
            ('new second title', 'new second content'),
            ('new third title', 'new third content'),
        ]
)
def test_create_post_default_published_true(
                    authorized_client,
                    add_user_db_id1,
                    add_fake_posts_db_userid1,
                    title,
                    content,
):
    response = authorized_client.post(
                'posts',
                json=dict(
                    title=title,
                    content=content,
                )
    )
    assert response.status_code == 201
    post = schemas.post.Post(**response.json())
    assert post.title == title
    assert post.content == content
    assert post.published == True
    assert post.owner_id == add_user_db_id1.id
    assert post.owner.email == add_user_db_id1.email

def test_unauthorized_create_post(unauthorized_client):
    response = unauthorized_client.post(
                        f'/posts',
                        json=dict(
                            title='nope',
                            content='nope'
                        )
    )
    assert response.status_code == 401

def test_unauthorized_delete_post(unauthorized_client, add_fake_posts_db_userid1):
    response = unauthorized_client.delete(f'/posts/{add_fake_posts_db_userid1[0].id}')
    assert response.status_code == 401

def test_delete_post(authorized_client, add_fake_posts_db_userid1):
    response = authorized_client.delete(f'/posts/{add_fake_posts_db_userid1[0].id}')
    assert response.status_code == 204

def test_delete_post_not_exist(authorized_client, add_fake_posts_db_userid1):
    response = authorized_client.delete(f'/posts/-1')
    assert response.status_code == 404

def test_delete_owned_post(authorized_client, token, session, add_fake_posts_db_multiple_users):
    tokendata = app.oauth2.verify_access_token(token, app.oauth2.unhautorized_exception)
    post: models.Post = (
        session.query(models.Post)
        .filter(models.Post.owner_id==tokendata.id)
        .first()
    )
    logger.info(post.content)
    response = authorized_client.delete(f'posts/{post.id}')
    assert response.status_code == 204
    # posts = session.query(models.Post).all()
    # assert len(posts) == 2
    check = session.query(models.Post).filter(models.Post.id==post.id).first()
    assert check is None

def test_delete_not_owned_post(authorized_client, token, session, add_fake_posts_db_multiple_users):
    tokendata = app.oauth2.verify_access_token(token, app.oauth2.unhautorized_exception)
    post: models.Post = (
        session.query(models.Post)
        .filter(models.Post.owner_id!=tokendata.id)
        .first()
    )
    logger.info(post.content)
    response = authorized_client.delete(f'posts/{post.id}')
    assert response.status_code == 403
    # posts = session.query(models.Post).all()
    # assert len(posts) == 2
    check = session.query(models.Post).filter(models.Post.id==post.id).first()
    assert check is not None
