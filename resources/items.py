from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.item import ItemModel
from schemas import ItemSchema, ItemUpdateSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError

# flask_smorest Blueprint is used to divide API into multiple segments
blp = Blueprint("items", __name__, description="Items API")



@blp.route("/items")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
         return ItemModel.query.all()

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
    
    def delete(self, id):
        item = ItemModel.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item Deleted."}, 200
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, request_data, id):
        item = ItemModel.query.get_or_404(id)
        item.name = request_data["name"]
        item.price = request_data["price"]
        db.session.add(item)
        db.session.commit()
        return item

