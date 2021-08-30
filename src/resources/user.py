
import sqlite3
from flask_restful import Resource, reqparse
from uuid import uuid4
from flask_jwt import jwt_required
from models.user import UserModel
from response_body import ResponseBody as Res
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
    def post(self):
        data = UserSignUp.parser.parse_args()
        if(UserModel.findByUsername(data["username"])):
            return Res(None, "A user with the given username has already exist", 400).__dict__, 400
        newUser = UserModel.insertUser(data)
        return Res(newUser, "User has been successfully create", 201).__dict__, 201
class GetAllUsers(Resource):
    # @jwt_required()
    def get(self):
        try:
            return Res(UserModel.getAllUsers(), "All existing users in the server", 200).__dict__, 200;
        except:
            return Res(None, "Cannot retrieve users", 500).__dict__, 500

class GetUser(Resource):
    def get(self, id):
        user = UserModel.findById(id)
        if(user):
            try:
                return Res(user, "Currently logged in user", 200).__dict__, 200
            except:
                return Res(None, "Cannot fetch currently logged in user", 500).__dict__, 500
        return Res(None, "User not found", 404).__dict__, 404