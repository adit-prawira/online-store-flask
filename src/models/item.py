import sqlite3
from uuid import uuid4
class ItemModel:
    def __init__(self, _id:str, name:str, price:float):
        self.id = _id
        self.name = name
        self.price = price
    
    @classmethod
    def findById(cls, _id:str):
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        connection.close()
        item = cls(*row) if row else None
        return item

    @classmethod
    def deleteById(cls, _id:str):
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE id=?"
        cursor.execute(query, (_id,))
        connection.commit()
        connection.close()
    
    @classmethod
    def updateItem(cls, newData:dict):
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        query = "UPDATE items SET name=?, price=? WHERE id=?"
        cursor.execute(query, (newData["name"], newData["price"], newData["id"]))
        connection.commit()
        connection.close()
    
    @classmethod
    def insertItem(cls, data:dict):
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        itemId = str(uuid4())
        query = "INSERT INTO items VALUES(?, ?, ?)"
        cursor.execute(query, (itemId, data["name"], data["price"]))
        connection.commit()
        connection.close()
        return {
            "name": data["name"],
            "price": data["price"],
            "id": itemId
        }
    
    @classmethod
    def getAllItems(cls):
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        keys = [header[0] for header in result.description]
        items = [dict(zip(keys, row)) for row in result.fetchall()]
        connection.close()
        return items