from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items
from helpers import responseHandler
from schemas import ItemSchema, ItemUpdateSchema


# flask_smorest Blueprint is used to divide API into multiple segments
blp = Blueprint("items", __name__, description="Items API")



@blp.route("/items")
class ItemList(MethodView):
    @responseHandler
    def get(self):
         return list(items.values())

    @blp.arguments(ItemSchema)
    @responseHandler
    def post(self, request_data):
        if(request_data["store_id"] not in stores):
            raise KeyError()
        
        id = len(items) + 1 
        new_item = {**request_data, "id": id}
        items[id] = new_item
        return new_item




@blp.route("/items/<int:id>")
class Item(MethodView):

    @responseHandler
    def get(self, id):
        item = items[id]
        return item

    @responseHandler
    def delete(self, id):
        del items[id]
        return True
    
    @blp.arguments(ItemUpdateSchema)
    @responseHandler
    def put(self, request_data, id):
        match = items[id]
        # i just manual set the name and price so we dont accidentally update the id
        match |= { "name": request_data["name"], "price": request_data["price"] }
        return match

