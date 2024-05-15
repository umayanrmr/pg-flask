from flask import Flask, request
from db import items, stores
from helpers import responseHandler

# variable name must be the same as the filename. which is app.py
app = Flask(__name__)

@app.get("/stores")
@responseHandler
def get_stores(): 
    return list(stores.values())


@app.post("/stores")
@responseHandler
def create_store():
    request_data = request.get_json()
    id = len(stores) + 1 
    new_item = {**request_data, "id": id }
    stores[id] = new_item
    return new_item


@app.get("/stores/<int:id>")
@responseHandler
def get_store(id): 
    store = stores[id]
    return store


@app.post("/items")
@responseHandler
def create_item():
    request_data = request.get_json()

    if(request_data["store_id"] not in stores):
        raise KeyError()
    
    id = len(items) + 1 
    new_item = {**request_data, "id": id}
    items[id] = new_item
    return new_item


@app.get("/items/<int:id>")
@responseHandler
def get_item(id): 
    item = items[id]
    return item


@app.get("/stores/<int:id>/items")
@responseHandler
def get_store_items(id): 
    print(items.values())
    return [item for item in items.values() if item['store_id'] == id]
