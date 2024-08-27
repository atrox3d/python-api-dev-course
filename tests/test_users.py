import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import event

from app.main import app
import schemas.user
# from app.config import sqlite_settings
from db.orm.sqlite import get_db, Base

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    '''
    ENFORCE SQLITE FOREIGN KEY
    https://stackoverflow.com/a/77708922
    '''
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
##################################################################

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///social.db"
# SQLALCHEMY_DATABASE_URL = sqlite_settings.database_url

# point to test db
SQLALCHEMY_DATABASE_URL = "sqlite:///testsocial.db"

# create engine, session and base pointing to test db
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=False
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# not needed, we use the original base
# Base = declarative_base()
# Base.metadata.create_all(bind=engine)

# create override Dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# override app dependecy with the new get_db which points to testdb
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    print()
    
    print(f'CLIENT FIXTURE| dropping tables')
    Base.metadata.drop_all(bind=engine)

    print(f'CLIENT FIXTURE| creating tables')
    Base.metadata.create_all(bind=engine)
    
    yield TestClient(app)

def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json().get('message') == 'welcome to my api'

def test_create_user(client):
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

