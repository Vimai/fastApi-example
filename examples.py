from typing import Optional
from fastapi import FastAPI, Header, HTTPException

from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/documentos}")
async def read_documento():
    return [{"documento_uuid": "uuid1"}, {"documento_uuid": "uuid1"}]


documents = {'1': '111', '2': '222'}


@app.get("/documentos/{documento_uuid}")
async def read_documento(documento_uuid):
    document = documents.get(documento_uuid)
    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"documento_uuid": documento_uuid}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


# Request body

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None  # optional


@app.post("/items/")
async def create_item(item: Item):
    return item


# Header

@app.get("/client")
async def read_client(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}