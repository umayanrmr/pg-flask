from flask import Flask, request


# variable name must be the same as the filename. which is app.py
app = Flask(__name__)


## FOR LIST
# def searchStore(items, name):
#     for item in items:
#         if(item["name"] == name):
#             return item
#     raise RuntimeError("Could not find store")

# stores = [
#     {
#         "name": "My Store 1",
#         "items": [
#             {
#                 "name": "Chair",
#                 "price": 15.99
#             }
#         ]

#     }
# ]



stores = {
    1: {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99
            }
        ]

    },
    2: {
        "name": "My Store 2",
        "items": [
            {
                "name": "Table",
                "price": 71
            }
        ]

    }
}

@app.get("/stores")
def get_stores(): 
    return { "data" : stores }


@app.post("/stores")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    id = len(stores) + 1 
    stores[id] = new_store
    return { "data": new_store }, 201




@app.post("/stores/<int:id>/items")
def create_item(id):
    try:
        request_data = request.get_json()
        new_item = {"name": request_data["name"], "price": request_data["price"]}
        stores[id]["items"].append(new_item)
        return { "data": new_item }, 201
    except RuntimeError as e:
        return {"message": e.__str__()}, 404



@app.get("/stores/<int:id>")
def get_store(id): 
    try:
        store = stores[id]
        return { "data": store } , 200
    except RuntimeError as e:
        return {"message": e.__str__()}, 404




@app.get("/stores/<int:id>/items")
def get_store_items(id): 
    try:
        store = stores[id]
        return { "data": store["items"] } , 200
    except RuntimeError as e:
        return {"message": e.__str__()}, 404
