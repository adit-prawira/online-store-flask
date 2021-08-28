from flask import Flask, request
from flask_restful import Resource, Api
from uuid import uuid4
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
app = Flask(__name__)
app.secret_key = "adit2899!!280199"
api = Api(app)

jwt = JWT(app, authenticate, identity) # creating the end point of /auth

items = []

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
        data = request.get_json()
        item = next(filter(lambda item: item["id"] == id, items), None)
        if(item):
            item["name"] = data["name"]
            item["price"] = data["price"]
            return item, 204 
        return {
                "message":"Item not found",
                "status": 404,
                "item": item
            }, 404
api.add_resource(Item, "/item/<string:id>")     

# Create an item to the store   
class CreateItem(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
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
api.add_resource(CreateItem, "/item")     

#Get all item list in the database
class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {"items": items}, 200
api.add_resource(ItemList, "/items")



app.run(port=5000, debug=True)