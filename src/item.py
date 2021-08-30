import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from uuid import uuid4
from response_body import ResponseBody as ResB

parser = reqparse.RequestParser()
parser.add_argument("name", 
    type=str,
    required=True,
    help="A name of an item must be provided."
)
parser.add_argument("price", 
    type=float,
    required=True,
    help="Price of the following item must be provided."
)

class Items:
    def __init__(self, _id, name, price):
        self.id = _id
        self.name = name
        self.price = price
    
    @classmethod
    def findById(cls, _id):
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        connection.close()
        item = cls(*row) if row else None
        return item

    @classmethod
    def deleteById(cls, _id):
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE id=?"
        cursor.execute(query, (_id,))
        connection.commit()
        connection.close()
        
# Get and update details of an item in the database by passing its id
class Item(Resource):
    @jwt_required()
    def get(self, id):
        item = Items.findById(id)
        if(item):
            return ResB(item.__dict__, "Item found in store", 200).__dict__, 200
        return ResB(item, "Item not found in store", 404).__dict__, 404
    
    @classmethod
    def updateItem(cls, id):
        global parser
        data = parser.parse_args()
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        query = "UPDATE items SET name=?, price=? WHERE id=?"
        cursor.execute(query, (data["name"], data["price"], id))
        connection.commit()
        connection.close()
        
    @jwt_required()
    def put(self, id):
        try:
            item = Items.findById(id)
            if(not item):
                return ResB(item, "Item not found", 404), 404
            self.updateItem(id)
            return ResB(Items.findById(id).__dict__, "Item successfully updated", 204).__dict__, 204
        except:
            return ResB(None, "An error has occur during update", 500).__dict__, 500

    @jwt_required()
    def delete(self, id):
        try:
            item = Items.findById(id)
            if(item):
                Items.deleteById(id)
                return ResB(None, "Item successfully deleted", 204).__dict__, 204
            return ResB(None, "Item not found", 404).__dict__, 404
        except:
            return ResB(None, "An error has occur during deletion", 500).__dict__, 500

# Create an item to the store   
class CreateItem(Resource):
    @classmethod
    def insertItem(cls):
        global parser
        data = parser.parse_args()
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        itemId = str(uuid4())
        query = "INSERT INTO items VALUES(?, ?, ?)"
        cursor.execute(query, (itemId, data["name"], data["price"]))
        connection.commit()
        connection.close()
        return {
            "name": data["name"],
            "price": data["price"],
            "id": itemId
        }
        
    @jwt_required()
    def post(self):
        try:
            item = self.insertItem()
            return ResB(item, "Item is successfully created", 201).__dict__, 201
        except:
            return ResB(None, "An error has occur during creation", 500).__dict__, 500

#Get all item list in the database
class ItemList(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        keys = [header[0] for header in result.description]
        items = [dict(zip(keys, row)) for row in result.fetchall()]
        connection.close()
        return ResB(items, "ALl existing items in store", 200).__dict__, 200