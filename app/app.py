from flask import Flask, Blueprint
from flask_restful import Api
from flask_jwt_extended import JWTManager
from .config import database_path
from datetime import timedelta

from sqlalchemy import delete
from app.Resources.Item import Item, ItemList
from app.Resources.store import Store, StoreList
from app.Resources.user import UserRegister
from app.Resources.user import User, UserLogin, TokenRefresh


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///{database_path}'
app.config["PROPAGATE_EXCEPTIONS"] = True

app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=1)

app.config['JWT_AUTH_USERNAME_KEY'] = 'username'

app.secret_key = "shiv"


v1 = Blueprint("v1", __name__, url_prefix="/v1")
base = Blueprint("base", __name__, url_prefix="/base")

api = Api(base)


jwt = JWTManager(app)



@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: # Instead of hard-coding, you should read from a config file or a database
        return {"is_admin": True}
    return {"is_admin": False}

@jwt.expired_token_loader
def expired_token_callback():
    return {"description": "The token has expired.",
            "error": "token_expired"}, 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {"description": "Signature verification failed.",
            "error": "invalid_token"}, 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return {"description": "Request does not contain an access token",
            "error": "authorization_required"}, 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(header, data):
    return {"description": "The token is not fresh.",
            "error": "fresh_token_required"}, 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return {"description": "The token has been revoked.",
            "error": "token_revoked"}, 401


#Api end points


api.add_resource(Item, "/item/<string:name>")
api.add_resource(Store, "/store/<string:name>")


api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")

api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")  #get, delete
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")

#blueprint register
v1.register_blueprint(base)
app.register_blueprint(v1)

