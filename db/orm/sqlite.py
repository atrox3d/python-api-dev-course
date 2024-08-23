# https://fastapi.tiangolo.com/tutorial/sql-databases

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from config import sqlite_settings

##################################################################
# ENFORCE SQLITE FOREIGN KEY
# https://stackoverflow.com/a/77708922
##################################################################
from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
##################################################################


# SQLALCHEMY_DATABASE_URL = "sqlite:///social.db"
SQLALCHEMY_DATABASE_URL = sqlite_settings.database_url
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

