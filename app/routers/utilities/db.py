import json
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel

from db.orm.sqlite import get_db
from db.orm import models

router = APIRouter(prefix='/db', tags=['util/db'])

@router.get('/')
def db():
    return {'db': 'welcome to the db utility'}


def get_tables_models(module) -> dict:
    return {model.__tablename__:model for model in
         [getattr(module, name) for name in dir(module)]
         if getattr(model, '__tablename__', None) is not None
         }

@router.get('/table/show/{tablename}')
def db(
        tablename:str,
        db: Session = Depends(get_db),
):
    try:
        model = get_tables_models(models)[tablename]
        rows = db.query(model).all()
        return {tablename: rows}
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{tablename=} not found'
        )

@router.get('/table/import/{tablename}/from/{filename}')
def db(
        tablename:str,
        filename:str,
        delete:bool=False,
        db: Session = Depends(get_db),
):
    print(tablename, filename, delete)
    try:
        model = get_tables_models(models)[tablename]

        if delete:
            db.query(model).delete()
        
        with open(filename) as fp:
            data = json.load(fp)
        for row in data:
            db.add(model(**row))
        db.commit()
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{tablename=} not found'
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{filename=} not found'
        )
    except json.decoder.JSONDecodeError as jde:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=repr(jde)
        )



