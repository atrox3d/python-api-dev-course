from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC

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

    print(f'TOKEN| {ACCESS_TOKEN_EXPIRE_MINUTES = }')
    print(f'TOKEN| {SECRET_KEY = }')
    print(f'TOKEN| {ALGORITHM  = }')
    print(f'TOKEN| {now        = }')
    print(f'TOKEN| {expire     = }')
    print(f'TOKEN| {to_encode  = }')
    print(f'TOKEN| {token      = }')

    return token

