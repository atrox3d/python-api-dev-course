from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC
from fastapi import Depends, Request, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


from db.orm import models
from db.orm.sqlite import get_db
import schemas
import schemas.user
from config import sqlite_settings

# SECRET_KEY
# alghorytm
# expiration time

# https://github.com/fastapi/fastapi/blob/0.68.0/docs_src/security/tutorial004.py
# to get a string like this run:
# openssl rand -hex 32
# SECRET_KEY = 'bdc7593632ada6a134bf519314cdb58e8f10680d21c9944374d87c62fb993914'
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = sqlite_settings.secret_key
ALGORITHM = sqlite_settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = sqlite_settings.access_token_expire_minutes

def create_access_token(data:dict):
    # https://youtu.be/0sOvCWFmrtA?si=yye34QX-bvHtUTL0&t=23570

    to_encode = data.copy()         # work on data shallow copy
    now = datetime.now(             # get current time
        # UTC                       # use UTC to get UTC time
    )
    
    delta = timedelta(              # time difference
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    expire = now + delta            # expire time
    
    to_encode['exp'] = expire       # add expire time to data
    
    token = jwt.encode(             # encode everything into token
                    to_encode,      # data payload + exp (+header????)
                    SECRET_KEY,
                    ALGORITHM
    )

    print(f'TOKEN|CREATE| {ACCESS_TOKEN_EXPIRE_MINUTES = }')
    print(f'TOKEN|CREATE| {SECRET_KEY = }')
    print(f'TOKEN|CREATE| {ALGORITHM  = }')
    print(f'TOKEN|CREATE| {now        = }')
    print(f'TOKEN|CREATE| {delta      = }')
    print(f'TOKEN|CREATE| {expire     = }')
    print(f'TOKEN|CREATE| {to_encode  = }')
    print(f'TOKEN|CREATE| {token      = }')

    return token

def verify_access_token(token:str, credentials_exception:Exception):
    
    print(f'TOKEN|VERIFY| {token    = }')
    
    try:
        print(f'TOKEN|VERIFY| decode token')
        payload = jwt.decode(                  # decode token, get only payload
                        token, 
                        SECRET_KEY, 
                        algorithms=[ALGORITHM]
        )
        print(f'TOKEN|VERIFY| {payload  = }')
        id = payload.get('user_id')
        print(f'TOKEN|VERIFY| {id       = }')
        if id is None:
            raise credentials_exception
        
        token_data = schemas.user.TokenData(id=id)
        print(f'TOKEN|VERIFY| {token_data  = }')

        return token_data

    except JWTError as jwte:
        print(f'TOKEN|VERIFY| {jwte       = }')
        raise credentials_exception

# create callable dependency to get token from 
# header "WWW-Authenticate": "Bearer"
oauth2_scheme = OAuth2PasswordBearer(
                        tokenUrl='login'
)

def get_current_user(
        token:str = Depends(oauth2_scheme),  # inject token,
        db: Session = Depends(get_db)
        # request: Request = Depends()
):
    print(f'GET_CURRENT_USER| {oauth2_scheme.__dict__ = }')
    # print(f'GET_CURRENT_USER| {oauth2_scheme() = }')
    print(f'GET_CURRENT_USER| create exception')
    unhautorized = HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='unhautorized: invalid credentials',
                        headers={"WWW-Authenticate": "Bearer"},
    )
    # https://youtu.be/0sOvCWFmrtA?si=Dh1sIirAYVL4Si4h&t=26702
    print(f'GET_CURRENT_USER| call verify_access_token')
    token = verify_access_token(token, unhautorized)
    print(f'GET_CURRENT_USER| {token = }')
    print(f'GET_CURRENT_USER| {token == 1 = }')
    # get user from db
    user: models.User = db.query(models.User)\
                        .filter(models.User.id == token.id)\
                        .first()

    print(f'GET_CURRENT_USER| { {c.name: getattr(user, c.name) for c in user.__table__.columns} }')
    # print(f'GET_CURRENT_USER| {schemas.user.UserDb.model_validate(user)}')

    return user
