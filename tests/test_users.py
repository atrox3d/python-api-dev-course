from fastapi.testclient import TestClient

from app.main import app
import schemas.user

client = TestClient(app)

def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json().get('message') == 'welcome to my api'

def test_create_user():
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

