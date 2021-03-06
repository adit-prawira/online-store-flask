
from flask_restful import Resource, reqparse
from uuid import uuid4
from models.user import UserModel
from response_body import ResponseBody as Res
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (create_access_token, 
                                create_refresh_token, 
                                jwt_required, get_jwt, 
                                get_jwt_identity)
from blacklist import BLACK_LIST
class UserSignUp(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", 
        type=str,
        required=True,
        help="A username must be provided."
    )
    parser.add_argument("password", 
        type=str,
        required=True,
        help="A password must be provided."
    )
    parser.add_argument("firstName", 
        type=str,
        required=True,
        help="A First name must be provided"
    )
    parser.add_argument("lastName", 
        type=str,
        required=False,
    )
    
    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        if(UserModel.findByUsername(data["username"])):
            return Res(None, "A user with the given username has already exist", 400).__dict__, 400
        data["id"] = str(uuid4())
        newUser = UserModel(data["id"], data["username"], 
                            data["password"], data["firstName"],
                            data["lastName"])
        newUser.saveToDB()
        data.pop("password")
        return Res(data, "User has been successfully create", 201).__dict__, 201
class GetAllUsers(Resource):
    @jwt_required()
    def get(self):
        try:
            return Res(UserModel.getAllUsers(), "All existing users in the server", 200).__dict__, 200;
        except:
            return Res(None, "Cannot retrieve users", 500).__dict__, 500

class GetUser(Resource):
    @jwt_required()
    def get(self, username):
        
        user = UserModel.findByUsername(username)
        if(user):
            return Res(user.toJSON(), "Currently logged in user", 200).__dict__, 200
        return Res(None, "User not found", 404).__dict__, 404
    
class UserSignIn(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", 
        type=str,
        required=True,
        help="A username must be provided."
    )
    parser.add_argument("password", 
        type=str,
        required=True,
        help="A password must be provided."
    )
    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        
        # find user in the database and check if the given password is valid
        user = UserModel.findByUsername(data["username"])
        if(user and safe_str_cmp(user.password, data["password"])):
            access_token = create_access_token(identity=user.id, fresh=True) # create access token
            refresh_token = create_refresh_token(user.id) # create refresh token
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        return Res(None, "Invalid credentials", 401).__dict__, 401
class UserSignOut(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLACK_LIST.add(jti)
        return Res(None, "Successfully signed out", 200).__dict__, 200
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        currentUser = get_jwt_identity()
        newToken = create_access_token(identity=currentUser, fresh=False)
        return {
            "access_token": newToken
        }, 200