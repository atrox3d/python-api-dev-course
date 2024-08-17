from jose import JWTError, jwt
from datetime import datetime, timedelta

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
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode['exp'] = expire
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token
