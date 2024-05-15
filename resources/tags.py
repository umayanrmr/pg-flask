from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.item import ItemModel
from models.store import StoreModel
from models.tag import TagModel
from schemas import ItemSchema, StoreSchema, StoreUpdateSchema, TagItemSchema, TagSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


# flask_smorest Blueprint is used to divide API into multiple segments
blp = Blueprint("Tags","tags", __name__, description="Tags API")




@blp.route("/tags/<int:id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, id):
         return TagModel.query.get_or_404(id)
    
    def delete(self, id):
        item = TagModel.query.get_or_404(id)

        if not item.items:
            db.session.delete(item)
            db.session.commit()
            return {"message": "Item Deleted."}, 200
    
        abort(400, message="Could not delete tag, make sure tag is not associated with any items.")

  



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




@blp.route("/items/<int:id>/tags/<int:tag_id>")
class LinkTagToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, id, tag_id):
        item = ItemModel.query.get_or_404(id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e: 
            abort(500, message="An error occured while inserting the tag.")
        return item
    
    @blp.response(200, TagItemSchema)
    def delete(self, id, tag_id):
        item = ItemModel.query.get_or_404(id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e: 
            abort(500, message="An error occured while inserting the tag.")
        return {"message": "Item removed from tag", "item": item, "tag": tag}