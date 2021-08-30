
import sqlite3
from uuid import uuid4
from database import db

class UserModel(db.Model):
    __tablename__= "users"
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    firstName = db.Column(db.String(80))
    lastName = db.Column(db.String(80))
    
    def __init__(self, _id, username, password, firstName, lastName):
        self.id = _id
        self.username = username
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
    
    def toJSON(self):
        return {
            "id":self.id,
            "username":self.username,
            "firstName":self.firstName,
            "lastName":self.lastName
        }    
    @classmethod
    def findByUsername(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def findById(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def getAllUsers(cls):
        return list(map(lambda user: user.toJSON(), cls.query.all()))

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()
        