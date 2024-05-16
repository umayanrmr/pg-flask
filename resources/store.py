from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.item import ItemModel
from models.store import StoreModel
from schemas import ItemSchema, StoreSchema, StoreUpdateSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required


# flask_smorest Blueprint is used to divide API into multiple segments
blp = Blueprint("Stores", "stores", __name__, description="Stores API")



@blp.route("/stores")
class StoreList(MethodView):
    @jwt_required()
    @blp.response(200, StoreSchema(many=True))
    def get(self):
         return StoreModel.query.all()


    @jwt_required()
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
    @jwt_required()
    @blp.response(200, StoreSchema)
    def get(self, id):
        item = StoreModel.query.get_or_404(id)
        return item


    @jwt_required()
    def delete(self, id):
        item = StoreModel.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item Deleted."}, 200
    
    @jwt_required()
    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, request_data, id):
        item = StoreModel.query.get_or_404(id)
        item.name = request_data["name"]
        db.session.add(item)
        db.session.commit()
        return item


@blp.route("/stores/<int:id>/items")
class StoreItems(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self, id):
        return ItemModel.query.filter(ItemModel.store_id == id).all()
