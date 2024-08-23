import json
from types import ModuleType
from typing import Callable
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel

from db.orm.sqlite import SessionLocal, get_db
from db.orm import models
import schemas.post
import schemas.user
import app.utils
import helpers.default_users

def get_tables_models(module) -> dict:
    return {
        model.__tablename__:model for model in
        [getattr(module, name) for name in dir(module)]
        if getattr(model, '__tablename__', None) is not None
    }


def delete_all(db, model):
        db.query(model).delete()

def import_table_from_json(
        db:Session,
        models:ModuleType,
        tablename:str,
        filename:str=None,
        json_provider:Callable=None,
        delete_existing:bool=False
):
    model = get_tables_models(models)[tablename]

    if delete_existing:
        delete_all(model)

    if filename is not None:
        with open(filename) as fp:
            data = json.load(fp)
        for row in data:
            db.add(model(**row))
        db.commit()
    elif json_provider is not None:
        pass
    else:
        raise ValueError(
            'at least one of filename, json_provider must have a value'
        )

def import_all(
        db:Session,
        models:ModuleType,
        *tablenames:str,
        # tablename:str,
        # filename:str=None,
        json_provider:Callable=None,
        delete_existing:bool=False
):
    for tablename in tablenames:
        filename = f'{tablename}.json'
        import_table_from_json(
            db,
            models,
            tablename,
            filename,
            json_provider,
            delete_existing=delete_existing
        )

def hash_passwords(
        db:Session,
        models:ModuleType,
):
    for row in db.query(models.User).all():
        hashed_password = app.utils.hash(row.password)
        # print(row.email, row.password, hashed_password)
        row.password = hashed_password
    db.commit()


def setup_db(
        db:Session,
        models:ModuleType,
        json_provider:Callable=None,
        delete_existing:bool=False

):
    delete_all(db, models.Post)
    delete_all(db, models.User)

    print(f'SETUP_DB| importing defaults')
    for user in helpers.default_users.default_users:
        db_user = models.User(**user.model_dump())
        db_user.password = app.utils.hash(user.password)
        db.add(db_user)
    db.commit()

    print(f'SETUP_DB| importing tables')
    import_all(
                db,
                models,
                'users',
                'posts',
                delete_existing=False
            )
    
    # print(f'SETUP_DB| hashing passwords')
    # hash_passwords(
    #             db,
    #             models,
    # )

    print(f'SETUP_DB| done')