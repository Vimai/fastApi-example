from fastapi import FastAPI

from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from routers import users

import aiohttp
import asyncio

app = FastAPI()

app.include_router(users.router)

session = None


@app.on_event('startup')
async def startup_event():
    global session
    session = aiohttp.ClientSession()


@app.on_event('shutdown')
async def shutdown_event():
    await session.close()


class City(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50, unique=True)
    timezone = fields.CharField(50)

    def current_time(self) -> str:
        return ''

    @classmethod
    async def get_current_time(cls, obj, session):
        async with session.get(f'http://worldtimeapi.org/api/timezone/{obj.timezone}') as response:
            result = await response.json()
            current_time = result.get('datetime') or ''
            obj.current_time = current_time

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
    cities = await City_Paydantic.from_queryset(City.all())
    global session
    tasks = []
    for city in cities:
        task = asyncio.create_task(City.get_current_time(city, session))
        tasks.append(task)

    await asyncio.gather(*tasks)

    return cities


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
