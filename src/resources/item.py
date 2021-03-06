from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from response_body import ResponseBody as Res
from models.item import ItemModel

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
parser.add_argument("storeId", 
    type=str,
    required=True,
    help="A store ID must be provided."
)
        
# Get and update details of an item in the database by passing its id
class Item(Resource):
    @jwt_required()
    def get(self, id):
        item = ItemModel.findById(id)
        if(item):
            return Res(item.toJSON(), "Item found in store", 200).__dict__, 200
        return Res(item, "Item not found in store", 404).__dict__, 404
        
    @jwt_required()
    def put(self, id):
        try:
            item = ItemModel.findById(id)
            if(not item):
                return Res(item, "Item not found", 404).__dict__, 404
            global parser
            data = parser.parse_args()
            item.name = data["name"]
            item.price = data["price"]
            item.saveToDB()
            return Res(data, "Item successfully updated", 204).__dict__, 204
        except:
            return Res(None, "An error has occur during update", 500).__dict__, 500

    @jwt_required()
    def delete(self, id):
        claims = get_jwt()
        if(claims["is_admin"]):
            return Res(None, "Admin privilege required", 401).__dict__, 401
        try:
            item = ItemModel.findById(id)
            if(item):
                item.deleteFromDB()
                return Res(None, "Item successfully deleted", 204).__dict__, 204
            return Res(None, "Item not found", 404).__dict__, 404
        except:
            return Res(None, "An error has occur during deletion", 500).__dict__, 500

# Create an item to the store   
class CreateItem(Resource):
    @jwt_required(fresh=True)
    def post(self):
        try:
            global parser
            data = parser.parse_args()
            item = ItemModel(data["name"], data["price"], data["storeId"]) # create new model
            item.saveToDB()
            return Res(item.toJSON(), "Item is successfully created", 201).__dict__, 201
        except:
            return Res(None, "An error has occur during creation", 500).__dict__, 500

#Get all item list in the database
class ItemList(Resource):
    @jwt_required()
    def get(self):
        try:
            return Res(ItemModel.getAllItems(), "All existing items in store", 200).__dict__, 200
            #return Res(ItemModel.getAllItemsNotComplete(), "All existing items in the store. Sign in for more information", 200).__dict__, 200
        except:
            return Res(None, "Error during fetching all items", 500).__dict__, 500


    