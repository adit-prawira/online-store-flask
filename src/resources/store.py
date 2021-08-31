from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from response_body import ResponseBody as Res
from models.store import StoreModel
parser = reqparse.RequestParser()
parser.add_argument("name", 
    type=str,
    required=True,
    help="A name of an item must be provided."
) 

class AccessStore(Resource):
    @jwt_required()
    def get(self, id):
        store = StoreModel.findById(id)
        if(store):
            return Res(store.toJSON(), "Store found in database", 200).__dict__, 200
        return Res(None, "Store not found in database", 404).__dict__, 404
    
    @jwt_required()
    def delete(self, id):
        store = StoreModel.findById(id)
        if(store):
            store.deleteFromDB()
            return Res(None, "Store successfully deleted from database", 204).__dict__, 204
        return Res(None, "Store not found in database", 404).__dict__, 404
        
class CreateStore(Resource):
    @jwt_required()
    def post(self):
        data = parser.parse_args()
        if(StoreModel.findByName(data["name"])):
            return Res(None, "A store with similar name has already exist", 400).__dict__, 400
        newStore = StoreModel(data["name"])
        newStore.saveToDB()
        return Res(newStore.toJSON(), "Store has successfully created", 201).__dict__, 201

class StoreList(Resource):
    def get(self):
        return Res(StoreModel.getAllStores(), "All existing stores in the database", 200).__dict__, 200