import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserSignUp, GetAllUsers, GetUser, UserSignIn
from resources.item import Item, CreateItem, ItemList
from resources.store import AccessStore, CreateStore, StoreList
from models.store import StoreModel
from models.user import UserModel
from database import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("POSTGRESQL_URL", "sqlite:///development_database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "adit2899!!280199"
api = Api(app)
jwt = JWTManager(app) 

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if(UserModel.findById(identity)): # Will be integrated with Admin user model in the future
        return {"is_admin": True}
    return {"is_admin": False}

api.add_resource(Item, "/item/<string:id>")     
api.add_resource(CreateItem, "/item")     
api.add_resource(ItemList, "/items")

api.add_resource(GetUser, "/user/<string:username>")
api.add_resource(GetAllUsers, "/users")
api.add_resource(UserSignUp, "/user/signup")
api.add_resource(UserSignIn, "/user/signin")
api.add_resource(AccessStore, "/store/<string:id>")
api.add_resource(CreateStore, "/store")
api.add_resource(StoreList, "/stores")

if __name__ == "__main__":
    db.init_app(app)
    @app.before_first_request
    def create_tables():
        db.create_all()
    app.run(port=5000, debug=True)