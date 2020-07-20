import sqlite3

conn = sqlite3.connect("contact.sqlite")

cursor = conn.cursor()
sql_query = """ CREATE TABLE cont(
    id integer PRIMARY KEY,
    name text NOT NULL,
    number text NOT NULL,
    year interger NOT NULL
)"""

cursor.execute(sql_query)