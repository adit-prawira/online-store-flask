import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from uuid import uuid4

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
            return {
                "data": item.__dict__,
                "message": "Item found in store",
                "status": 200
            }, 200
        return {
            "data": item,
            "message": "Item not found in store",
            "status": 404
        },404
        
    @jwt_required()
    def put(self, id):
        item = Items.findById(id)
        if(not item):
            return {
                "data": item,
                "message":"Item not found",
                "status": 404,
            }
        global parser
        data = parser.parse_args()
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        query = "UPDATE items SET name=?, price=? WHERE id=?"
        cursor.execute(query, (data["name"], data["price"], id))
        connection.commit()
        connection.close()
        return {
            "data": Items.findById(id).__dict__,
            "message": "Item successfully updated.",
            "status": 204
        }, 204

    @jwt_required()
    def delete(self, id):
        item = Items.findById(id)
        if(item):
            Items.deleteById(id)
            return {"message": "Item successfully deleted", "status": 204}, 204
        return {"message": "Item not found", "status": 404}, 404

# Create an item to the store   
class CreateItem(Resource):
    @jwt_required()
    def post(self):
        global parser
        data = parser.parse_args()
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        itemId = str(uuid4())
        query = "INSERT INTO items VALUES(?, ?, ?)"
        cursor.execute(query, (itemId, data["name"], data["price"]))
        connection.commit()
        connection.close()
        item = {
            "name": data["name"],
            "price": data["price"],
            "id": itemId
        }
        return {
            "data": item,
            "message": "Item is successfully created",
            "status": 201
        }, 201

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
        return {"items": items}, 200