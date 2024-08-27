import schemas.user
import tests.database
from tests.database import client, session


DEBUG = False
def debug(*args, force=False, **kwargs):
    if DEBUG or force:
        print(*args, **kwargs)

tests.database.debug = debug

# session fixture is cached
def test_root(client, session):
    debug(f'\nTEST_ROOT| {session.rand = }', force=False)
    response = client.get('/')
    assert response.status_code == 200
    assert response.json().get('message') == 'welcome to my api'

# session fixture is cached
def test_create_user(client, session):
    debug(f'\nTEST_CREATE_USER| {session.rand = }', force=False)
    debug()
    debug(f'TEST_CREATE_USER| get_user')
    response = client.post(
                        '/users',
                        json={
                            'email': 'testuser@gmail.com',
                            'password': 'password'
                        }
    )
    assert response.status_code == 201
    user = schemas.user.UserOut(**response.json())
    assert user.email == 'testuser@gmail.com'

# session fixture is cached
def test_login_user(client, session):
    debug(f'\nTEST_LOGIN_USER| {session.rand = }', force=False)
    debug()
    debug(f'TEST_LOGIN_USER| get_user')
    response = client.post(
                        '/login',
                        data={
                            'username': 'testuser@gmail.com',
                            'password': 'password'
                        }
    )
    print(response)
    print(response.json())
    # assert response.status_code == 200
    # user = schemas.user.UserOut(**response.json())
    # assert user.email == 'testuser@gmail.com'

