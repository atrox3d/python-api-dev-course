import json
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel

from db.orm.sqlite import get_db
from db.orm import models
import helpers.db

router = APIRouter(prefix='/db', tags=['util/db'])

@router.get('/')
def db():
    return {'db': 'welcome to the db utility'}


@router.get('/table/show/{tablename}')
def db(
        tablename:str,
        db: Session = Depends(get_db),
):
    try:
        model = helpers.db.get_tables_models(models)[tablename]
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
        helpers.db.import_table_from_json(
            db,
            models,
            tablename,
            filename,
            delete_existing=delete
        )
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



@router.get('/table/import/all')
def db(
        delete:bool=False,
        db: Session = Depends(get_db),
):
    try:
        helpers.db.import_all(
            db,
            models,
            'users',
            'posts',
            delete_existing=delete
        )

    except KeyError as ke:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=repr(ke)
        )
    except FileNotFoundError as fnfe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=repr(fnfe)
        )
    except json.decoder.JSONDecodeError as jde:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=repr(jde)
        )
