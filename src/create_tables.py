import sqlite3
connection = sqlite3.connect("development_database.db")
cursor = connection.cursor()
query = "CREATE TABLE IF NOT EXISTS users(id string, username text, password text, firstName text, lastName text)"
cursor.execute(query)
connection.commit()
connection.close()