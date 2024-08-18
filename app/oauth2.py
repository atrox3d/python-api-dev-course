from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC

import schemas
import schemas.user

# SECRET_KEY
# alghorytm
# expiration time

# https://github.com/fastapi/fastapi/blob/0.68.0/docs_src/security/tutorial004.py
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = 'bdc7593632ada6a134bf519314cdb58e8f10680d21c9944374d87c62fb993914'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict):
    # work on data shallow copy
    to_encode = data.copy()
    # get current time
    now = datetime.now(
        # UTC\
    )
    # time difference
    delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # expire time
    expire = now + delta
    # add expire time to data
    to_encode['exp'] = expire
    # encode everything
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

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
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
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
    
    