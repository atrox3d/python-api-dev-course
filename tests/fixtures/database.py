import random
from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from sqlalchemy import event
import logging

import sqlalchemy.orm.session
from app.main import app
from db.orm.sqlite import get_db, Base
from tests.debug import debug

logger = logging.getLogger(__name__)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    '''
    ENFORCE SQLITE FOREIGN KEY
    https://stackoverflow.com/a/77708922
    '''
    # logger.debug('=' * 80)
    logger.debug('ENFORCE SQLITE FOREIGN KEY')
    # logger.debug('https://stackoverflow.com/a/77708922')
    # logger.debug('=' * 80)
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
logger.info('create engine')
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=False
)
logger.info('create TestingSessionLocal')
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
    # prepare db for testing
    logger.debug(f'dropping tables')
    Base.metadata.drop_all(bind=engine)
    logger.debug(f'creating tables')
    Base.metadata.create_all(bind=engine)

    logger.debug(f'creating session')
    db = TestingSessionLocal()
    try:
        logger.debug(f'yielding session')
        db.rand = random.random()       # check unique fixture
        logger.debug(f'{db.rand = }')
        yield db
    finally:
        logger.debug(f'SESSION FIXTURE| closing session')
        db.close()

@pytest.fixture
def unauthorized_client(session:Session) -> Generator[TestClient, None, None]:
    logger.debug(f'using session fixture')
    logger.debug(f'{session.rand = }')
    def override_get_db():
        try:
            logger.debug(f'yielding session')
            yield session
        finally:
            logger.debug(f'closing session')
            session.close()
    
    logger.debug(f'overriding get_db')
    app.dependency_overrides[get_db] = override_get_db
    
    logger.debug(f'yielding new test client')
    yield TestClient(app)
    # leave db untouched after test
