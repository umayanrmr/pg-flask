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

@app.put("/stores/<int:id>")
@responseHandler
def update_store(id):
    request_data = request.get_json()
    match = stores[id]
    print(match)
    # i just manual set the name and price so we dont accidentally update the id
    match |= { "name": request_data["name"] }
    return match


@app.get("/stores/<int:id>")
@responseHandler
def get_store(id): 
    store = stores[id]
    return store


@app.delete("/stores/<int:id>")
@responseHandler
def delete_store(id): 
    del stores[id]
    return True



@app.get("/stores/<int:id>/items")
@responseHandler
def get_store_items(id): 
    print(items.values())
    return [item for item in items.values() if item['store_id'] == id]



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



@app.get("/items")
@responseHandler
def get_items(): 
    return list(items.values())


@app.delete("/items/<int:id>")
@responseHandler
def delete_item(id): 
    del items[id]
    return True

@app.get("/items/<int:id>")
@responseHandler
def get_item(id): 
    item = items[id]
    return item


@app.put("/items/<int:id>")
@responseHandler
def update_item(id):
    request_data = request.get_json()
    match = items[id]
    # i just manual set the name and price so we dont accidentally update the id
    match |= { "name": request_data["name"], "price": request_data["price"] }
    return match

