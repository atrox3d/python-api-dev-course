import pytest
import schemas, schemas.user

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
