from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from db.orm.sqlite import get_db
import schemas.user
import db.orm.models as models
import app.utils
import app.oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(
            # not using pydantic: # credentials:schemas.user.UserLogin, 
            # using form data
            credentials:OAuth2PasswordRequestForm = 
                    Depends(),      # get username+password from form data
                                    # instead of JSON
            db: Session = Depends(get_db)
) -> schemas.user.Token:
    print(f'LOGIN| credentials = {credentials.__dict__}')
    print(f'LOGIN| {credentials.username = }')
    print(f'LOGIN| {credentials.password = }')

    # find user inside db using name|email|...
    user: models.User = db.query(models.User).filter(
                models.User.email==credentials.username
        ).first()
    # print(f'LOGIN| user = { {c.name:getattr(user, c.name) for c in user.__table__.columns}} ')
    # check if user found in db
    if user:
        print(f'LOGIN| {user.id         = }')
        print(f'LOGIN| {user.email      = }')
        print(f'LOGIN| {user.password   = }')
        print(f'LOGIN| {user.created_at = }')
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='invalid credentials')
    
    # check that hashed passwords match
    if not app.utils.verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            details='invalid credentials')
    
    # create encoded token containing 
    #   - user_id: user_id
    #   - exp    : token expiration time
    #   - header ?????
    token = app.oauth2.create_access_token(
        {
            'user_id': user.id,
            # add fields as necessary
        }
    )
    # return JSON with encoded token
    # return {'token': token, 'token_type': 'bearer'}
    return schemas.user.Token(
        access_token=token,
        token_type='bearer'
    )



