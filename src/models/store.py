from database import db
from uuid import uuid4
class StoreModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship("ItemModel", lazy="dynamic") # do not create object for each item in the relationship yet
    def __init__(self, name):
        self.id = str(uuid4())
        self.name = name
    def toJSON(self):
        return {
            "id": self.id,
            "name": self.name,
            "items": list(map(lambda item: item.toJSON(), self.items.all()))
        }
        
    @classmethod
    def findById(cls, _id):
        return cls.query.filter_by(id=_id).first()
    @classmethod
    def findByName(cls, _name):
        return cls.query.filter_by(name=_name).first()
    @classmethod
    def getAllStores(cls):
        return list(map(lambda store: store.toJSON(), cls.query.all()))
    
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()
    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()
        
        