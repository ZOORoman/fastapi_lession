
from datetime import datetime
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationError
from fastapi.responses import JSONResponse

app = FastAPI(
    title="TriPic"
)

fake_users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "triper", "name": "Robert"},
    {"id": 3, "role": "hiker", "name": "Sergey", "degree": [
        {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "expert"}
    ]},
]

@app.get("/")
def get_hello():
    return "Hello world"

class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"

class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType

class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []

@app.get("/users/{user_id}", response_model=List[User])
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]

fake_avia = [
    {"id": 1, "user_id": 1, "froms": "Moscow", "to": "Milan", "price": 7854, "status": True},
    {"id": 2, "user_id": 1, "froms": "Moscow", "to": "Berlin", "price": 13567, "status": False},
    {"id": 3, "user_id": 1, "froms": "Moscow", "to": "Barcelona", "price": 11503, "status": True},
]

class Avia(BaseModel):
    id: int
    user_id: int
    froms: str = Field(max_length=10)
    to: str
    price: float = Field(ge=0)
    status: bool


@app.post("/avias")
def add_avia(avias: List[Avia]):
    fake_avia.extend(avias)
    return {"status": 200, "data": fake_avia}

# @app.get("/avia")
# def get_avia(limit: int = 10, offset: int = 0):
#     return fake_avia[offset:][:limit]


# fake_users2 = [
#     {"id": 1, "role": "admin", "name": "Bob"},
#     {"id": 2, "role": "triper", "name": "Robert"},
#     {"id": 3, "role": "hiker", "name": "Sergey"},
# ]

# @app.post("/users/{user_id}")
# def change_user_name(user_id: int, new_name: str):
#     current_user = list(filter(lambda user: user.get("id") == user_id, fake_users2))[0]
#     current_user["name"] = new_name
#     return {"status": 200, "data": current_user}
