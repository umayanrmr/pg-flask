from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from helpers import responseHandler
from models.item import ItemModel
from schemas import ItemSchema, ItemUpdateSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError

# flask_smorest Blueprint is used to divide API into multiple segments
blp = Blueprint("items", __name__, description="Items API")



@blp.route("/items")
class ItemList(MethodView):
    @responseHandler
    def get(self):
         return list(items.values())

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, request_data):
        item = ItemModel(**request_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError: 
            abort(500, message="An error occured while inserting the item")
        
        return item
    

@blp.route("/items/<int:id>")
class Item(MethodView):

    @blp.response(200,ItemSchema)
    def get(self, id):
        item = ItemModel.query.get_or_404(id)
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

