from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import event
import sqlalchemy.orm.session
from app.main import app
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
# def override_get_db():
    # db = TestingSessionLocal()
    # try:
        # yield db
    # finally:
        # db.close()

# override app dependecy with the new get_db which points to testdb
# app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def session() -> Generator[sqlalchemy.orm.session.Session, None, None]:
    print()
    
    # prepare db for testing
    print(f'SESSION FIXTURE| dropping tables')
    Base.metadata.drop_all(bind=engine)
    print(f'SESSION FIXTURE| creating tables')
    Base.metadata.create_all(bind=engine)

    print(f'SESSION FIXTURE| creating session')
    db = TestingSessionLocal()
    try:
        print(f'SESSION FIXTURE| yielding session')
        yield db
    finally:
        print()
        print(f'SESSION FIXTURE| closing session')
        db.close()

@pytest.fixture
def client(session) -> Generator[TestClient, None, None]:
    print(f'CLIENT FIXTURE| using session fixture')
    def override_get_db():
        # db = TestingSessionLocal()
        try:
            print(f'OVERRIDE_GET_DB| yielding session')
            yield session
        finally:
            print()
            print(f'OVERRIDE_GET_DB| closing session')
            session.close()
    
    print(f'CLIENT FIXTURE| overriding get_db')
    app.dependency_overrides[get_db] = override_get_db
    
    print(f'CLIENT FIXTURE| yielding new test client')
    yield TestClient(app)
    # leave db untouched after test
