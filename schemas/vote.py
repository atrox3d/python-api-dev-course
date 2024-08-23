from pydantic import BaseModel, EmailStr, conint
from datetime import datetime as dt

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=0) # type: ignore

