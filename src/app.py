from flask import Flask, request
from flask_restful import Resource, Api
from uuid import uuid4
#res = next((sub for sub in test_list if sub['is'] == 7), None)
app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
    def get(self, id):
        for item in items:
            if(item["id"] == id):
                name = item["name"]
                searchedItem = item
                searchedItem["message"] = f"{name} is found in store"
                searchedItem["status"] = 200
                return searchedItem, 200
        return {
                "message":"Item not found",
                "status": 404,
                "item": None
            }, 404
        
    def put(self, id):
        data = request.get_json()
        for item in items:
            if(item["id"] == id):
                item["name"] = data["name"]
                item["price"] = data["price"]
                return item, 204
        return {
                "message":"Item not found",
                "status": 404,
                "item": None
            }, 404
        
class CreateItem(Resource):
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
        
class ItemList(Resource):
    def get(self):
        return {"items": items}, 200
    
api.add_resource(CreateItem, "/item")
api.add_resource(Item, "/item/<string:id>")
api.add_resource(ItemList, "/items")
app.run(port=5000)