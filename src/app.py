from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from user import UserSignUp
from item import Item, CreateItem, ItemList

app = Flask(__name__)
app.secret_key = "adit2899!!280199"
api = Api(app)

jwt = JWT(app, authenticate, identity) # creating the end point of /auth

api.add_resource(Item, "/item/<string:id>")     
api.add_resource(CreateItem, "/item")     
api.add_resource(ItemList, "/items")
api.add_resource(UserSignUp, "/user/signup")

app.run(port=5000, debug=True)