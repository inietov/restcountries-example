import sqlite3

connection = sqlite3.connect("thisdot_example.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS countries(name text, data text)")