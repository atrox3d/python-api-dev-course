# https://fastapi.tiangolo.com/tutorial/sql-databases

from types import ModuleType
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import schemas

SQLALCHEMY_DATABASE_URL = "sqlite:///social.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
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

def reset_db(
                models:ModuleType, 
                default_posts:schemas.Posts,
                default_users:schemas.Users,
                drop_tables:bool=False
):
    _db = SessionLocal()

    if drop_tables:
        print('MAIN| dropping table posts')
        models.User.__table__.drop(engine)
        models.Post.__table__.drop(engine)
        print('MAIN| dropping table users')
        models.User.__table__.create(engine)
        models.Post.__table__.create(engine)
        _db.commit()

    print('MAIN| deleting all users')
    _db.query(models.User).delete()
    for user in default_users:
        print(f'MAIN| adding {user}')
        new_user = models.User(**user.model_dump())
        _db.add(new_user)
        _db.commit()
    _db.close()
