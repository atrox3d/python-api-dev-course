import pytest

import schemas.user
import tests.database
from tests.database import client, session
import app.oauth2



DEBUG = False
def debug(*args, force=False, **kwargs):
    if DEBUG or force:
        print(*args, **kwargs)

tests.database.debug = debug

@pytest.fixture
def user_create() -> schemas.user.UserCreate:
    ''' returns a UserCreate instance for validation/input'''
    return schemas.user.UserCreate(
        email='testuser@gmail.com',
        password='password'
    )

@pytest.fixture
def user_create_json(user_create) -> dict[str, str]:
    ''' returns json of user_create '''
    return user_create.model_dump()

@pytest.fixture
def user_login_json(user_create) -> dict[str, str]:
    ''' returns converted user_create for login '''
    return {
        'username': user_create.email, 
        'password': user_create.password
    }

@pytest.fixture
def new_user(client, user_create, user_create_json) -> schemas.user.UserDb:
    ''' creates new user and return model of it from db '''
    response = client.post(
                        '/users',
                        json=user_create_json
    )
    assert response.status_code == 201
    userdb = schemas.user.UserDb(
        **response.json(),
        password=user_create.password
    )
    return userdb


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
def test_login(client, session, user_login_json, new_user):
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
    token = schemas.user.Token(
        **response.json()
    )
    tokendata = app.oauth2.verify_access_token(
        token.access_token,
        app.oauth2.unhautorized_exception
    )
    assert tokendata.id == new_user.id

