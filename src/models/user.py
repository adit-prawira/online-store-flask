
import sqlite3
from uuid import uuid4

class UserModel:
    def __init__(self, _id, username, password, firstName, lastName):
        self.id = _id
        self.username = username
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        
    @classmethod
    def __removePassword(cls, data):
        if(data):
            data.pop("password")
    @classmethod
    def findByUsername(cls, username):
        connection  = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        
        # get all users from table and only select those with maching username
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone() # get the first value from the filtered table
        connection.close()
        user = cls(*row).__dict__ if row else None
        cls.__removePassword(user)
        return user
    
    @classmethod
    def findById(cls, _id):
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        connection.close()
        user = cls(*row).__dict__ if row else None
        print(user)
        cls.__removePassword(user)
        return user

    @classmethod
    def getAllUsers(cls):
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        query = "SELECT * FROM users"
        result = cursor.execute(query)
        keys = [header[0] for header in result.description]
        users = [dict(zip(keys, values)) for values in result.fetchall()]
        connection.close()
        [cls.__removePassword(user) for user in users]
        return users

    @classmethod
    def insertUser(cls, data:dict):
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES(?, ?, ?, ?, ?)"
        cursor.execute(query, (str(uuid4()), data["username"], data["password"], data["firstName"], data["lastName"]))
        connection.commit()
        connection.close()
        cls.__removePassword(data)
        return data