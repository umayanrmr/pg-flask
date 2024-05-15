from flask import Flask, request


# variable name must be the same as the filename. which is app.py
app = Flask(__name__)



def searchStore(items, name):
    for item in items:
        if(item["name"] == name):
            return item
    raise RuntimeError("Could not find store")

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99
            }
        ]

    }
]


@app.get("/stores")
def get_stores(): 
    return { "data" : stores }


@app.post("/stores")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return { "data": new_store }, 201




@app.post("/stores/<string:name>/items")
def create_item(name):
    try:
        request_data = request.get_json()
        new_item = {"name": request_data["name"], "price": request_data["price"]}
        store = searchStore(stores, name)
        store["items"].append(new_item)
        return { "data": new_item }, 201
    except RuntimeError as e:
        return {"message": e.__str__()}, 404



@app.get("/stores/<string:name>")
def get_store(name): 
    try:
        store = searchStore(stores, name)
        return { "data": store } , 200
    except RuntimeError as e:
        return {"message": e.__str__()}, 404




@app.get("/stores/<string:name>/items")
def get_store_items(name): 
    try:
        store = searchStore(stores, name)
        return { "data": store["items"] } , 200
    except RuntimeError as e:
        return {"message": e.__str__()}, 404
