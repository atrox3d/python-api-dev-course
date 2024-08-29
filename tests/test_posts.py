import json

# from app.routers import posts
import tests.debug
import schemas.post


def  setup_module():
    tests.debug.DEBUG = True

def test_get_all_posts(authorized_client, add_fake_posts):
    response = authorized_client.get('/posts')
    assert response.status_code == 200
    # posts = [schemas.post.PostOut(**post) for post in response.json()]
    # [print(post) for post in posts]
    # posts = response.json()
    print(json.dumps(response.json(), indent=2))
    posts = [schemas.post.Post(**post.get('Post')) for post in response.json()]
    assert len(posts) == len(add_fake_posts)
    for post, dbpost in zip(posts, add_fake_posts):
        assert post.id == dbpost.id
        assert post.title == dbpost.title
        assert post.content == dbpost.content
        assert post.published == dbpost.published
        assert post.created_at == dbpost.created_at
        assert post.owner_id == dbpost.owner_id

def test_unauthorized_get_all_posts(client, add_fake_posts):
    response = client.get('/posts')
    assert response.status_code == 401

def test_unauthorized_get_one_posts(client, add_fake_posts):
    response = client.get(f'/posts/{add_fake_posts[0].id}')
    assert response.status_code == 401

