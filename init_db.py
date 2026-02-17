import sqlite3

conn = sqlite3.connect("userdata.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password BLOB NOT NULL,
    rol TEXT NOT NULL DEFAULT 'user'
)
""")

conn.commit()
conn.close()

print("DB lista con columna rol ✅")
