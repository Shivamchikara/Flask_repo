from flask_restful import Resource, reqparse
from app.Model.user_model import UserModel
import hmac

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username", type=str, required=True, help= "username can't be null")
_user_parser.add_argument("password", type=str, required=True, help= "password required")

class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data["username"]):
            return {"message": "username already exists"}

        user = UserModel(**data)
        user.save_to_db()
        return {"message": "user registered"}


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "user not found"}
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "user not found"}
        user.delete_from_db()
        return {"message": "user deleted"}


class UserLogin(Resource):
    @classmethod
    def post(cls):

        data = _user_parser.parse_args()
        user = UserModel.find_by_username(username=data["username"])

        if user and hmac.compare_digest(user.password, data["password"]):

            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            return {"access_token": access_token,
                    "refresh_token": refresh_token}
        return {"message": "Invalid credentials"}


class TokenRefresh(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}