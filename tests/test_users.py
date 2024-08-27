import pytest

import schemas.user
import tests.database
from tests.database import client, session



DEBUG = False
def debug(*args, force=False, **kwargs):
    if DEBUG or force:
        print(*args, **kwargs)

tests.database.debug = debug

@pytest.fixture
def user_create() -> schemas.user.UserCreate:
    return schemas.user.UserCreate(
        email='testuser@gmail.com',
        password='password'
    )

@pytest.fixture
def user_create_json(user_create) -> dict[str, str]:
    return user_create.model_dump()

@pytest.fixture
def user_login_json(user_create) -> dict[str, str]:
    return {
        'username': user_create.email, 
        'password': user_create.password
    }

# session fixture is cached
def test_root(client, session):
    debug(f'\nTEST_ROOT| {session.rand = }', force=False)
    response = client.get('/')
    assert response.status_code == 200
    assert response.json().get('message') == 'welcome to my api'

# session fixture is cached
def test_create_user(client, session, user_create_json):
    debug(f'\nTEST_CREATE_USER| {session.rand = }', force=False)
    debug()
    debug(f'TEST_CREATE_USER| get_user')
    response = client.post(
                        '/users',
                        json=user_create_json
    )
    assert response.status_code == 201
    user = schemas.user.UserOut(**response.json())
    assert user.email == 'testuser@gmail.com'

# session fixture is cached
def test_login_user(client, session, user_login_json):
    debug(f'\nTEST_LOGIN_USER| {session.rand = }', force=False)
    debug()
    debug(f'TEST_LOGIN_USER| get_user')
    print(user_login_json)
    response = client.post(
                        '/login',
                        data=user_login_json
    )
    print(response)
    print(response.json())
    # assert response.status_code == 200
    # user = schemas.user.UserOut(**response.json())
    # assert user.email == 'testuser@gmail.com'

