from typing import Optional
from fastapi import FastAPI, Header, HTTPException

from pydantic import BaseModel

app = FastAPI()


class City(BaseModel):
    name: str
    timezone: str


db = []


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/cities")
async def get_cities():
    return db


@app.get("/cities/{city_id}")
async def read_item(city_id: int):
    return db[city_id - 1]


@app.post("/cities/")
async def create_city(city: City):
    db.append(city.dict())
    return db[-1]


@app.delete("/cities/{city_id}")
async def delete_city(city_id: int):
    db.pop(city_id - 1)
    return {}
