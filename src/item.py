from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from uuid import uuid4

items = []
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

# Get and update details of an item in the database by passing its id
class Item(Resource):
    @jwt_required()
    def get(self, id):
        item = next(filter(lambda item: item["id"] == id, items), None)
        if(item):
            name = item["name"]
            item["message"] = f"{name} is found in store"
            item["status"] = 200
            return item, 200
        return {
                "message":"Item not found",
                "status": 404,
                "item": item
            }, 404
        
    @jwt_required()
    def put(self, id):
        global parser
        data = parser.parse_args()
        item = next(filter(lambda item: item["id"] == id, items), None) # take the first element of the list
        if(item):
            item["name"] = data["name"]
            item["price"] = data["price"]
            return item, 204 
        return {
                "message":"Item not found",
                "status": 404,
                "item": item
            }, 404
        
    @jwt_required()
    def delete(self, id):
        global items
        items= list(filter(lambda item: item["id"] != id, items)) # return list of all item that doesn't have tha passed id
        return {"message": "Item successfully deleted", "status": 204}, 204

# Create an item to the store   
class CreateItem(Resource):
    @jwt_required()
    def post(self):
        global parser
        data = parser.parse_args()
        item = {
            "name": data["name"],
            "price": data["price"],
            "id": str(uuid4())
        }
        items.append(item)
        name = data["name"]
        item["message"] = f"{name} is created"
        item["status"] = 201
        return item, 201

#Get all item list in the database
class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {"items": items}, 200