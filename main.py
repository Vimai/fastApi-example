from typing import Optional
from fastapi import FastAPI, Header, HTTPException

from pydantic import BaseModel

from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

import requests

app = FastAPI()


class City(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50, unique=True)
    timezone = fields.CharField(50)

    def current_time(self) -> str:
        r = requests.get(f'http://worldtimeapi.org/api/timezone/{self.timezone}')
        response = r.json()
        current_time = response.get('datetime') or ''
        return current_time

    class PydanticMeta:
        computed = ('current_time', )


City_Paydantic = pydantic_model_creator(City, name='City')
CityIn_Paydantic = pydantic_model_creator(City, name='CityIn', exclude_readonly=True)

db = []


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/cities")
async def get_cities():
    response = await City_Paydantic.from_queryset(City.all())
    return response


@app.get("/cities/{city_id}")
async def read_item(city_id: int):
    return await City_Paydantic.from_queryset_single(City.get(id=city_id))


@app.post("/cities/")
async def create_city(city: CityIn_Paydantic):
    city_obj = await City.create(**city.dict(exclude_unset=True))
    return await City_Paydantic.from_tortoise_orm(city_obj)


@app.delete("/cities/{city_id}")
async def delete_city(city_id: int):
    await City.filter(id=city_id).delete()
    return {}

register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)
