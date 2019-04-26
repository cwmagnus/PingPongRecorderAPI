from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import *
from models.user import UserModel
from blacklist import BLACKLIST
from passlib.hash import bcrypt

# Set up request fields
_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "username",
    type = str,
    required = True,
    help = "This field cannot be blank."
)
_user_parser.add_argument(
    "email",
    type = str,
    required = True,
    help = "This field cannot be blank."
)
_user_parser.add_argument(
    "password",
    type = str,
    required = True,
    help = "This field cannot be blank."
)

# Register a new user
class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with that username already exists"}, 400

        elif UserModel.find_by_email(data["email"]):
            return {"message": "A user with that email address already exists"}, 400

        user = UserModel(data["username"], data["email"], bcrypt.hash(data["password"]))
        user.save_to_db()

        return {"message": "User created successfully."}, 201

# Login a user
class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data["username"])

        if user and bcrypt.verify(data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       "access_token": access_token,
                       "refresh_token": refresh_token
                   }, 200

        return {"message": "Invalid Credentials!"}, 401

# Logout a user
class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200

# Refresh the users access token
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200