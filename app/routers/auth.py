from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from db.orm.sqlite import get_db
import schemas.user
import db.orm.models as models
import app.utils
import app.oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(credentials:schemas.user.UserLogin, db: Session = Depends(get_db)):
    user: models.User = db.query(models.User).filter(
        models.User.email==credentials.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='invalid credentials')
    
    if not app.utils.verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details='invalid credentials')
    
    token = app.oauth2.create_access_token(
        {
            'user_id': user.id
        }
    )
    return {'token': token, 'token_type': 'bearer'}




