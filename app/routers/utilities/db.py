from fastapi import HTTPException, status, Depends, APIRouter

router = APIRouter(prefix='/db', tags=['util/db'])

@router.get('/')
def db():
    return {'db': 'hello'}
