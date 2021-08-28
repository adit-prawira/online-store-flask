
import sqlite3
from flask_restful import Resource, reqparse
from uuid import uuid4
from flask_jwt import jwt_required
class UserModel:
    def __init__(self, _id, username, password, firstName, lastName):
        self.id = _id
        self.username = username
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
    
    @classmethod
    def findByUsername(cls, username):
        connection  = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        
        # get all users from table and only select those with maching username
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone() # get the first value from the filtered table
        connection.close()
        user = cls(*row) if row else None
        return user
    
    @classmethod
    def findById(cls, _id):
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        user = cls(*row) if row else None
        connection.close()
        return user

    @classmethod
    def getAll(cls):
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        query = "SELECT * FROM users"
        result = cursor.execute(query)
        keys = [header[0] for header in result.description]
        users = [dict(zip(keys, values)) for values in result.fetchall()]
        connection.close()
        return users

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
            return {"message": "A user with the given username has already exist.", "status": 400}, 400
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