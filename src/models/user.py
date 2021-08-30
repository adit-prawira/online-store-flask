
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