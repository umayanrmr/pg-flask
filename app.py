import os
from flask import Flask, jsonify
from flask_smorest import Api

from db import db
import models

from flask_jwt_extended import JWTManager



from models.user import UserModel
from resources.items import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tags import blp as TagsBlueprint
from resources.users import blp as UserBlueprint

from blocklist import BLOCKLIST

# variable name must be the same as the filename. which is app.py




def create_app(db_url=None):
    app = Flask(__name__)


    
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] =  db_url or os.getenv("DATABASE_URL", "sqlite:///data.db") 
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    api = Api(app)


    app.config["JWT_SECRET_KEY"] = "1b9795864d205ff97886a860fb03164b"
    jwt = JWTManager(app)


    # this function will be called everytime that a route with that requires FRESH TOKEN receives a NON FRESH Token
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (jsonify({"message": "This action requires a fresh token.", "error": "token_fresh_required"}),401)
    

    # this function will be called everytime that the app receives a token
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist_callback(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    # this function will be called everytime that a jwt is revoked, in short if the token_in_blocklist_loader returns true, this will run
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (jsonify({"message": "The token has been revoked.", "error": "token_revoked"}),401)

    # customize EXPIRED token message
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (jsonify({"message": "The token has expired.", "error": "token_expired"}),401)
    
    # customize INVALID token message
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (jsonify({"message": "Signature verification failed.", "error": "token_invalid"}),401)

    # customize MISSING token message
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (jsonify({"description": "Request does not contain an access token.","error": "token_required"}),401)
    

    # this function will be called anytime flask_jwt_extended.create_access_token is called
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity): # identity is the id of the user, create_access_token(identity=user.id)
        user = UserModel.query.filter(UserModel.id == identity).first()
        # you can add role here
        return { "is_admin": True, "role": "Jesus" }
        # print(user)



    with app.app_context():
        db.create_all()

   
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagsBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
