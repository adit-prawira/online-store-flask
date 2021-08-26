from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)
stores = [
    {
        "name":"seven-eleven",
        "storeId":str(uuid4()),
        "items":[
            {
                "name":"Indomie",
                "price": 5.99,
                "itemId": str(uuid4())
            }
        ]
    }
]

def binarySearch(arr, name):
    low = 0;
    mid = len(arr) - 1
    high = 0
    while low <= high:
        mid = (high + low)//2
        if(arr[mid]["name"] < name):
            low = mid + 1
        elif(arr[mid]["name"] > name):
            high = mid - 1
        else:
            return arr[mid]
    return -1
    
# create a new store
@app.route("/store", methods=["POST"])
def createStore():
    requestData = request.get_json()
    newStore = {
        "name":requestData["name"],
        "items":[],
        "storeId":str(uuid4())
    }
    stores.append(newStore)
    return jsonify(newStore)

# get a specific store
@app.route("/store/<string:name>")
def getStore(name:str):
    store = binarySearch(stores, name)
    if(store == -1):
        return jsonify({
        "error":{
            "status": 404,
            "message":"Store not found"
        }
    })
        
    return jsonify(binarySearch(stores, name))

# get all existing store in the server
@app.route("/store")
def getStores():
    return jsonify({"stores":stores}) # jsonify can only read dictionary not a list

@app.route("/store/<string:name>/item", methods=["POST"])
def createItem(name:str):
    store = binarySearch(stores, name)
    if(store == -1):
        return jsonify({
        "error":{
            "status": 404,
            "message":"Store not found"
        }
    })
    requestData = request.get_json()
    newItem = {
        "name": requestData["name"],
        "price": requestData["price"],
        "itemId": str(uuid4())
    }
    store["items"].append(newItem)
    return jsonify({"items":store["items"]})
    

@app.route("/store/<string:name>/item")
def getItems(name:str):
    store = binarySearch(stores, name)

    if(store == -1):
        return jsonify({
        "error":{
            "status": 404,
            "message":"Item not found"
        }
    })
    return jsonify({"items":store["items"]})

app.run(port=5000)