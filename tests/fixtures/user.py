from typing import Generator
from fastapi.testclient import TestClient
import pytest
import logging

import schemas, schemas.user
from app import oauth2
from .database import unauthorized_client

logger = logging.getLogger(__name__)

@pytest.fixture
def user_creation_schema(fake_users_creation_dict) -> schemas.user.UserCreate:
    ''' returns a UserCreate instance for validation/input'''
    logger.debug('creating UserCreate from 1st fake dict')
    return schemas.user.UserCreate(
        **fake_users_creation_dict[0]
    )

@pytest.fixture
def user_creation_json(user_creation_schema) -> dict[str, str]:
    ''' returns json of user_create '''
    logger.debug('creating json from 1st fake dict')
    return user_creation_schema.model_dump()

@pytest.fixture
def user_login_json(user_creation_schema) -> dict[str, str]:
    ''' returns converted user_create for login '''
    logger.debug('creating json user creation creds from 1st fake dict')
    return {
        'username': user_creation_schema.email, 
        'password': user_creation_schema.password
    }

@pytest.fixture
def add_user_db(unauthorized_client, user_creation_schema, user_creation_json) -> schemas.user.UserDb:
    ''' creates new user and return model of it from db '''
    logger.debug('creating 1st user')
    response = unauthorized_client.post(
                        '/users',
                        json=user_creation_json
    )
    assert response.status_code == 201
    userdb = schemas.user.UserDb(
        **response.json(),
        password=user_creation_schema.password
    )
    return userdb

@pytest.fixture
def add_users_db(request, add_user_db,  unauthorized_client, fake_users_creation_dict) -> schemas.user.UserDb:
    logger.debug('creating remaining user')
    new_users = []
    # if 'add_user_db' in request.fixturenames:
    # users = fake_users_creation_dict[1:]
    # else:
        # users = fake_users_creation_dict
    
    for user_creds in fake_users_creation_dict[1:]:
        ''' creates new user and return model of it from db '''
        response = unauthorized_client.post(
                            '/users',
                            json=user_creds
        )
        assert response.status_code == 201
        userdb = schemas.user.UserDb(
            **response.json(),
            password=user_creds['password']
        )
        new_users.append(userdb)
    return new_users

@pytest.fixture
def token(add_user_db) -> str:
    logger.debug('creating acces token')
    return oauth2.create_access_token({'user_id': add_user_db.id})

@pytest.fixture
def authorized_client(unauthorized_client, token) -> Generator[TestClient, None, None]:
    logger.debug('creating authorized client')
    unauthorized_client.headers = {
        **unauthorized_client.headers,
        'Authorization': f'Bearer {token}'
    }
    yield unauthorized_client