from datetime import datetime as dt
from schemas.user import UserCreate, Users


default_users: Users = [
    UserCreate(email='fab@gmail.com', password='meow'),
]

