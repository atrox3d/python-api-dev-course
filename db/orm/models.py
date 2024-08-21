from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
import sqlalchemy
from sqlalchemy.sql.sqltypes import TIMESTAMP
# from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func
import sqlalchemy as sa
from .sqlite import Base
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, 
                    #    default=True,
                       server_default='true'
                       )
    created_at = Column(TIMESTAMP(timezone=True),   # timestamp data type
                        nullable=False,
                        server_default=func.now())  # server side timestamp
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                      nullable=False)
    
    owner = relationship('User')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),   # timestamp data type
                        nullable=False,
                        server_default=func.now())  # server side timestamp
