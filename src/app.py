from flask import Flask
from flask_restful import Api
import os
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserSignUp, GetAllUsers, GetUser
from resources.item import Item, CreateItem, ItemList
from resources.store import AccessStore, CreateStore, StoreList
from models.store import StoreModel
from database import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("POSTGRESQL_URL", "sqlite:///development_database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "adit2899!!280199"
api = Api(app)
    
jwt = JWT(app, authenticate, identity) # creating the end point of /auth

api.add_resource(Item, "/item/<string:id>")     
api.add_resource(CreateItem, "/item")     
api.add_resource(ItemList, "/items")

api.add_resource(GetUser, "/user/<string:username>")
api.add_resource(GetAllUsers, "/users")
api.add_resource(UserSignUp, "/user/signup")

api.add_resource(AccessStore, "/store/<string:id>")
api.add_resource(CreateStore, "/store")
api.add_resource(StoreList, "/stores")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)