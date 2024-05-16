from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from blocklist import BLOCKLIST
from models.user import UserModel
from schemas import UserSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, jwt_required


# flask_smorest Blueprint is used to divide API into multiple segments
blp = Blueprint("Users","users", __name__, description="User API")


@blp.route("/users")
class Users(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
         jwt = get_jwt()

         if not jwt.get("role") == "Jesus":
            abort(401, message="Jesus priviledge required")


         return UserModel.query.all()

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, request_data):
        if UserModel.query.filter(UserModel.username == request_data["username"]).first():
            abort(409, message="A user with that username already exists.")
        item = UserModel(
            username=request_data["username"],
            password=pbkdf2_sha256.hash(request_data["password"])
        )  
        db.session.add(item)
        db.session.commit()
        return item
    

@blp.route("/users/<int:id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, id):
         return UserModel.query.get_or_404(id)
    

    @jwt_required(fresh=True) # every destructive URL must require a fresh=True token
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





@blp.route("/login")
class Login(MethodView):
    @blp.arguments(UserSchema)
    def post(self,request_data):

        user = UserModel.query.filter(UserModel.username == request_data["username"]).first()
        if user == None:
            abort(401, message="Could not find user")
        
        if pbkdf2_sha256.verify(request_data["password"], user.password) == False:
            abort(401, message="Invalid credentials")

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        return { "access_token": access_token, "refresh_token": refresh_token }

        
@blp.route("/logout")
class Logout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return { "message": "Successfully logged out" }, 200



@blp.route("/refresh")
class Refresh(MethodView):
    # refresh=True tells python that it needs refresh token, not access token
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity() # or get_jwt().get("sub")


        # add refresh to the blocklist so it cant be used again
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)

        new_token = create_access_token(identity=current_user, fresh=False)
        refresh_token = create_refresh_token(identity=current_user)
        return { "access_token": new_token, "refresh_token": refresh_token }


        