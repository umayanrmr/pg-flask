from flask import Flask, request
from db import items, stores, getStore
from helpers import responseHandler

# variable name must be the same as the filename. which is app.py
app = Flask(__name__)

@app.get("/stores")
@responseHandler
def get_stores(): 
    return stores


@app.post("/stores")
@responseHandler
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    id = len(stores) + 1 
    stores[id] = new_store
    return new_store


@app.get("/stores/<int:id>")
@responseHandler
def get_store(id): 
    store = stores[id]
    return store


@app.post("/stores/<int:id>/items")
@responseHandler
def create_item(id):
    request_data = request.get_json()
    new_item = {"name": request_data["name"], "price": request_data["price"]}
    store = stores[id]
    store["items"].append(new_item)
    return new_item


@app.get("/stores/<int:id>/items")
@responseHandler
def get_store_items(id): 
    store = stores[id]
    return store["items"]
