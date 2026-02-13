import sqlite3

# Script para crear la base de datos y la tabla usuarios
def init_database():
    connection = sqlite3.connect('usuarios.db')
    cursor = connection.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'cliente'
        )
    ''')
    
    connection.commit()
    connection.close()
    print("Base de datos y tabla 'usuarios' creadas exitosamente.")

if __name__ == '__main__':
    init_database()
