
import sqlite3
from flask_restful import Resource, reqparse
from uuid import uuid4
from flask_jwt import jwt_required
from models.user import UserModel

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
            return {
                "message": "A user with the given username has already exist.", 
                "status": 400
            }, 400
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES(?, ?, ?, ?, ?)"
        cursor.execute(query, (str(uuid4()), data["username"], data["password"], data["firstName"], data["lastName"]))
        connection.commit()
        connection.close()
        return {
            "message": "User has been successfully create",
            "status": 201
        }, 201

class GetAllUsers(Resource):
    @jwt_required()
    def get(self):
        return {"users":UserModel.getAll()}