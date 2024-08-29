import pytest

import schemas.user
# import tests.database
# from tests.database import client, session
import app.oauth2
from tests.debug import debug
import tests.debug


def  setup_module():
    tests.debug.DEBUG = True

# session fixture is cached
def test_root(unauthorized_client, session):
    debug(f'\nTEST_ROOT| {session.rand = }', force=False)
    response = unauthorized_client.get('/')
    assert response.status_code == 200
    assert response.json().get('message') == 'welcome to my api'

# session fixture is cached
def test_create_user(unauthorized_client, session, user_creation_json):
    debug(f'\nTEST_CREATE_USER| {session.rand = }', force=False)
    debug()
    debug(f'TEST_CREATE_USER| get_user')
    response = unauthorized_client.post(
                        '/users',
                        json=user_creation_json
    )
    assert response.status_code == 201
    user = schemas.user.UserOut(**response.json())
    assert user.email == 'testuser@gmail.com'

# session fixture is cached
def test_login(unauthorized_client, session, user_login_json, new_user_db):
    debug(f'\nTEST_LOGIN_USER| {session.rand = }', force=False)
    debug()
    debug(f'TEST_LOGIN_USER| get_user')
    print(user_login_json)
    response = unauthorized_client.post(
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
    assert tokendata.id == new_user_db.id

