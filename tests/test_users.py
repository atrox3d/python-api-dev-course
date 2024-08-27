from fastapi.testclient import TestClient
from app.main import app

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
    print(response.json())
    assert response.status_code == 201

