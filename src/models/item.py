import sqlite3
from uuid import uuid4
from database import db
class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    
    def __init__(self, _id:str, name:str, price:float):
        self.id = _id
        self.name = name
        self.price = price
        
    @classmethod
    def findById(cls, _id:str):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def getAllItems(cls):
        return list(map(lambda item: item.toJSON(), cls.query.all()))
    
    
    def toJSON(self):
        return {"id":self.id, "name":self.name, "price":self.price}
    
    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()
        
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()
        
    
