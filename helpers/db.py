import json
from types import ModuleType
from typing import Callable
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel

from db.orm.sqlite import Base, SessionLocal, get_db
from db.orm import models
import schemas.post
import schemas.user
import app.utils
import helpers.default_users

def get_tables_models_from_module(module) -> dict:
    return {
        model.__tablename__:model for model in
        [getattr(module, name) for name in dir(module)]
        if getattr(model, '__tablename__', None) is not None
    }

def get_model_from_tablename(tablename:str, module:ModuleType):
    return get_tables_models_from_module(module)[tablename]

def delete_all_records(db, model):
        db.query(model).delete()

def load_json_into_table(db:Session, filename:str, model):
    print(f'LOAD_JSON_INTO_TABLE| loading {filename}')
    with open(filename) as fp:
        data = json.load(fp)

    print(f'LOAD_JSON_INTO_TABLE| loading rows into table')
    for row in data:
        db.add(model(**row))
    db.commit()

def import_table_from_json(
        db:Session,
        models:ModuleType,
        tablename:str,
        filename:str=None,
        json_provider:Callable=None,
):
    print(f'IMPORT_TABLE_FROM_JSON| getting model')
    model = get_model_from_tablename(tablename, models)

    if filename is not None:
        print(f'IMPORT_TABLE_FROM_JSON| loading {filename} into {tablename}')
        load_json_into_table(db, filename, model)
    elif json_provider is not None:
        raise NotImplementedError
    else:
        raise ValueError(
            'at least one of filename, json_provider must have a value'
        )

def import_all(
        db:Session,
        models:ModuleType,
        *tablenames:str,
        json_provider:Callable=None,
):
    for tablename in tablenames:
        filename = f'{tablename}.json'
        print(f'IMPORT_ALL| importing {filename} into {tablename}')
        import_table_from_json(
            db,
            models,
            tablename,
            filename,
            json_provider,
        )

def hash_passwords(
        db:Session,
        models:ModuleType,
):
    for row in db.query(models.User).all():
        print(f'HASH_PASSWORDS| hashing password for {row.email}')
        hashed_password = app.utils.hash(row.password)
        row.password = hashed_password
    db.commit()


def setup_db(
        db:Session,
        models:ModuleType,
        json_provider:Callable=None,
):
    print(f'SETUP_DB| deleting posts')
    delete_all_records(db, models.Post)

    print(f'SETUP_DB| deleting users')
    delete_all_records(db, models.User)

    print(f'SETUP_DB| importing default users')
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
                json_provider=json_provider
            )
    
    print(f'SETUP_DB| done')
