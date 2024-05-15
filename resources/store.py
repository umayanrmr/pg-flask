from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items
from helpers import responseHandler
from schemas import StoreSchema, StoreUpdateSchema


# flask_smorest Blueprint is used to divide API into multiple segments
blp = Blueprint("stores", __name__, description="Stores API")



@blp.route("/stores")
class StoreList(MethodView):
    @responseHandler
    def get(self):
         return list(stores.values())

    @blp.arguments(StoreSchema)
    @responseHandler
    def post(self, request_data):
        id = len(stores) + 1 
        new_item = {**request_data, "id": id }
        stores[id] = new_item
        return new_item
    

@blp.route("/stores/<int:id>")

class Store(MethodView):
    @responseHandler
    def get(self, id):
        store = stores[id]
        return store

    @responseHandler
    def delete(self, id):
        del stores[id]
        return True
    

    @blp.arguments(StoreUpdateSchema)
    @responseHandler
    def put(self, request_data, id):
        request_data = request.get_json()
        match = stores[id]
        print(match)
        # i just manual set the name and price so we dont accidentally update the id
        # |= just like the mapper in c#, it will only update the values existing in the right side
        match |= { "name": request_data["name"] }
        return match


@blp.route("/stores/<int:id>/items")
class StoreItems(MethodView):
    @responseHandler
    def get(self, id):
        print(items.values())
        return [item for item in items.values() if item['store_id'] == id]
