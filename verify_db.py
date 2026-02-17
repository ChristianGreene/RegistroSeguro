import sqlite3

conn = sqlite3.connect("userdata.db")
cursor = conn.cursor()

cursor.execute("SELECT id, email, rol FROM usuarios")
print(cursor.fetchall())

conn.close()
