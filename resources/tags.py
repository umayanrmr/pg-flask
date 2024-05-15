from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.item import ItemModel
from models.store import StoreModel
from models.tag import TagModel
from schemas import ItemSchema, StoreSchema, StoreUpdateSchema, TagSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


# flask_smorest Blueprint is used to divide API into multiple segments
blp = Blueprint("Tags","tags", __name__, description="Tags API")




@blp.route("/tags/<int:id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, id):
         return TagModel.query.get_or_404(id)

  



@blp.route("/stores/<int:store_id>/tags")
class StoreTags(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
         return TagModel.query.filter(TagModel.store_id == store_id).all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, request_data, store_id):
        item = TagModel(**request_data)
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Tag name already exists.")
        except SQLAlchemyError as e: 
            abort(500, str(e))
        return item
    