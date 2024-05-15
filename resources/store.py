from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from helpers import responseHandler
from models.store import StoreModel
from schemas import ItemSchema, StoreSchema, StoreUpdateSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


# flask_smorest Blueprint is used to divide API into multiple segments
blp = Blueprint("stores", __name__, description="Stores API")



@blp.route("/stores")
class StoreList(MethodView):
    @responseHandler
    def get(self):
         return list(stores.values())

    @blp.arguments(StoreSchema)
    @blp.response(201, ItemSchema)
    def post(self, request_data):
        item = StoreModel(**request_data)
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Store name already exists.")
        except SQLAlchemyError: 
            abort(500, message="An error occured while inserting the item")
        return item
    

@blp.route("/stores/<int:id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, id):
        item = StoreModel.query.get_or_404(id)
        return item

    @responseHandler
    def delete(self, id):
        item = StoreModel.query.get_or_404(id)
        raise NotImplementedError("")
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
