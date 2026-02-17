import sqlite3
import bcrypt

class RegistroUsuario:
    """Módulo de lógica para el registro seguro de usuarios"""

    def __init__(self, db_name='userdata.db'):
        self.db_name = db_name

    def validar_credenciales(self, email, password):
        # Validar email
        if not email or '@' not in email:
            return False, "Email inválido"

        # Validar longitud de contraseña (8-10 caracteres)
        if not password or len(password) < 8 or len(password) > 10:
            return False, "Credenciales Invalidas"

        return True, ""

    def usuario_existe(self, email):
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
            resultado = cursor.fetchone()
            connection.close()
            return resultado is not None
        except sqlite3.Error as e:
            print(f"Error de base de datos: {e}")
            return False

    def hashear_contrasena(self, password):
        salt = bcrypt.gensalt(rounds=12)
        hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hash_password  # bytes para BLOB ✅

    def registrar_usuario(self, email, password):
        # Validar credenciales
        es_valido, mensaje_error = self.validar_credenciales(email, password)
        if not es_valido:
            return {'status': False, 'codigo': 400, 'mensaje': mensaje_error}

        # Verificar si el usuario ya existe
        if self.usuario_existe(email):
            return {'status': False, 'codigo': 409, 'mensaje': 'El usuario ya existe'}

        # Hashear la contraseña
        password_hash = self.hashear_contrasena(password)

        # Guardar en la base de datos
        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO usuarios (email, password, rol) VALUES (?, ?, ?)',
                (email, password_hash, 'cliente')
            )
            connection.commit()
            connection.close()

            return {'status': True, 'codigo': 201, 'mensaje': 'Usuario Registrado'}

        except sqlite3.Error as e:
            return {'status': False, 'codigo': 500, 'mensaje': f'Error en la base de datos: {str(e)}'}

    # ==========================
    # ✅ NUEVO: Actualizar password
    # ==========================
    def actualizar_password(self, email, password_actual, password_nueva):
        # Validaciones básicas
        if not email or '@' not in email:
            return {'status': False, 'codigo': 400, 'mensaje': 'Email inválido'}

        if not password_actual or not password_nueva:
            return {'status': False, 'codigo': 400, 'mensaje': 'Datos incompletos'}

        # Mantener tu regla 8-10 caracteres
        if len(password_nueva) < 8 or len(password_nueva) > 10:
            return {'status': False, 'codigo': 400, 'mensaje': 'Credenciales Invalidas'}

        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()

            # 1) Buscar el hash guardado
            cursor.execute("SELECT password FROM usuarios WHERE email = ?", (email,))
            fila = cursor.fetchone()

            if not fila:
                connection.close()
                return {'status': False, 'codigo': 404, 'mensaje': 'Usuario no encontrado'}

            hash_guardado = fila[0]  # bytes (BLOB)

            # 2) Verificar password actual
            if not bcrypt.checkpw(password_actual.encode('utf-8'), hash_guardado):
                connection.close()
                return {'status': False, 'codigo': 401, 'mensaje': 'Contraseña actual incorrecta'}

            # 3) Hashear password nueva
            nuevo_hash = bcrypt.hashpw(password_nueva.encode('utf-8'), bcrypt.gensalt(rounds=12))

            # 4) Actualizar en DB
            cursor.execute(
                "UPDATE usuarios SET password = ? WHERE email = ?",
                (nuevo_hash, email)
            )

            connection.commit()
            connection.close()

            return {'status': True, 'codigo': 200, 'mensaje': 'Contraseña actualizada correctamente'}

        except sqlite3.Error as e:
            return {'status': False, 'codigo': 500, 'mensaje': f'Error en la base de datos: {str(e)}'}

    # ==========================
    # ✅ NUEVO: Actualizar rol
    # ==========================
    def actualizar_rol(self, email, rol):
        if not email or '@' not in email:
            return {'status': False, 'codigo': 400, 'mensaje': 'Email inválido'}

        if not rol:
            return {'status': False, 'codigo': 400, 'mensaje': 'Datos incompletos'}

        rol = rol.lower().strip()

        # Puedes dejar estos roles permitidos (ajusta si tu profe pide otros)
        roles_validos = {"cliente", "user", "admin"}
        if rol not in roles_validos:
            return {'status': False, 'codigo': 400, 'mensaje': 'Rol inválido (usa: cliente, user o admin)'}

        try:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()

            # Verificar que exista el usuario
            cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
            if not cursor.fetchone():
                connection.close()
                return {'status': False, 'codigo': 404, 'mensaje': 'Usuario no encontrado'}

            # Actualizar rol
            cursor.execute(
                "UPDATE usuarios SET rol = ? WHERE email = ?",
                (rol, email)
            )

            connection.commit()
            connection.close()

            return {'status': True, 'codigo': 200, 'mensaje': 'Rol actualizado correctamente'}

        except sqlite3.Error as e:
            return {'status': False, 'codigo': 500, 'mensaje': f'Error en la base de datos: {str(e)}'}
