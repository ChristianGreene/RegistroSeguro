import sqlite3

# Conectarse a la base de datos y mostrar los usuarios registrados
connection = sqlite3.connect('usuarios.db')
cursor = connection.cursor()

cursor.execute('SELECT id, email, password, role FROM usuarios')
usuarios = cursor.fetchall()

print("\n" + "="*80)
print("CONTENIDO DE LA TABLA USUARIOS")
print("="*80)
print(f"{'ID':<5} | {'Email':<30} | {'Password (Hash)':<40} | {'Role':<10}")
print("-"*80)

for usuario in usuarios:
    id_usuario, email, password_hash, role = usuario
    # Mostrar solo los primeros y últimos caracteres del hash
    hash_truncado = f"{password_hash[:10]}...{password_hash[-10:]}"
    print(f"{id_usuario:<5} | {email:<30} | {hash_truncado:<40} | {role:<10}")

print("-"*80)
print(f"Total de usuarios registrados: {len(usuarios)}")
print("="*80 + "\n")

connection.close()
