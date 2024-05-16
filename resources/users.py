from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.user import UserModel
from schemas import UserSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256


# flask_smorest Blueprint is used to divide API into multiple segments
blp = Blueprint("Users","users", __name__, description="User API")


@blp.route("/users")
class Users(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
         return UserModel.query.all()

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, request_data):
        item = UserModel(**request_data)
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Username name already exists.")
        except SQLAlchemyError: 
            abort(500, message="An error occured while inserting the item")
        return item
    


@blp.route("/users/<int:id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, id):
         return UserModel.query.get_or_404(id)
    
    def delete(self, id):
        item = UserModel.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item Deleted."}, 200

    # @blp.arguments(UserSchema)
    # @blp.response(200, UserSchema)
    # def put(self, request_data, id):
    #     item = StoreModel.query.get_or_404(id)
    #     item.name = request_data["name"]
    #     db.session.add(item)
    #     db.session.commit()
    #     return item

