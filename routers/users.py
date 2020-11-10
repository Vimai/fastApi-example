from typing import Optional
from fastapi import APIRouter

from pydantic import BaseModel
from pymongo import MongoClient


router = APIRouter()


class Users(BaseModel):
    name: str
    age: int
    city: Optional[str] = None  # optional


@router.get("/users/", tags=["users"])
async def read_users():
    client = MongoClient(host='localhost',
                              port=27017,
                              username='root',
                              password='password')
    db = client.projectdb
    users = db.users
    results = users.find({})
    return results


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
