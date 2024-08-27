import schemas.user
from .database import client, session

def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json().get('message') == 'welcome to my api'

def test_create_user(client, session):
    print()
    print(f'TEST_CREATE_USER| use client, session')
    # from db.orm import models
    # session.query(models.User).all()
    print(f'TEST_CREATE_USER| get_user')
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

