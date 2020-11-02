from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/documentos}")
async def read_documento():
    return [{"documento_uuid": "uuid1"}, {"documento_uuid": "uuid1"}]


@app.get("/documentos/{documento_uuid}")
async def read_documento(documento_uuid):
    return {"documento_uuid": documento_uuid}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]
