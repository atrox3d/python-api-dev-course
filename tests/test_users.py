import logging
from fastapi.testclient import TestClient

import schemas.user
import app.oauth2

logger = logging.getLogger(__name__)

# session fixture is cached
def test_root(
        unauthorized_client: TestClient, 
        session: app.oauth2.Session
):
    logger.debug(f'{session.rand = }')
    response = unauthorized_client.get('/')
    assert response.status_code == 200
    assert response.json().get('message') == 'welcome to my api'

# session fixture is cached
def test_create_user(
        unauthorized_client: TestClient, 
        session: app.oauth2.Session, 
        user_creation_json: dict[str, str]
):
    logger.debug(f'{session.rand = }')
    logger.debug(f'get_user')
    response = unauthorized_client.post(
                        '/users',
                        json=user_creation_json
    )
    assert response.status_code == 201

    user = schemas.user.UserOut(**response.json())
    assert user.email == 'testuser@gmail.com'

# session fixture is cached
def test_login(
        unauthorized_client: TestClient, 
        session: app.oauth2.Session, 
        user_login_json: dict[str, str], 
        add_user_db_id1: schemas.user.UserDb
):
    logger.debug(f'{session.rand = }')
    logger.debug(f'get_user')
    response = unauthorized_client.post(
                        '/login',
                        data=user_login_json
    )
    token = schemas.user.Token(**response.json())
    tokendata = app.oauth2.verify_access_token(
        token.access_token,
        app.oauth2.unhautorized_exception
    )
    assert tokendata.id == add_user_db_id1.id

