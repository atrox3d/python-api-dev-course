from fastapi import APIRouter, Body, Depends, status, HTTPException, Response
from pydantic import BaseModel


class Data(BaseModel):
    name: str
    age: int

router = APIRouter(prefix='/example', tags=['example'])

@router.post('')
def example(
                data:Data,              # pydantic: body params: JSON
                count:int = Body(),     # Body(): JSON
                queryparam: str=None    # none of the above: queryparam
    ):
    # JSON
    # {
    #     "data": {
    #         "name": "NAME",
    #         "age": 20
    #     },
    #     "count": 5
    # }
    print(data, count, queryparam)

