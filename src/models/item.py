import sqlite3
class ItemModel:
    def __init__(self, _id, name, price):
        self.id = _id
        self.name = name
        self.price = price
    
    @classmethod
    def findById(cls, _id):
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        connection.close()
        item = cls(*row) if row else None
        return item

    @classmethod
    def deleteById(cls, _id):
        connection = sqlite3.connect("development_database.db")
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE id=?"
        cursor.execute(query, (_id,))
        connection.commit()
        connection.close()