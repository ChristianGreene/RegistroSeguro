from flask import Flask, request, jsonify
from registro_logica import RegistroUsuario

import os
from dotenv import load_dotenv
import jwt
import datetime
from functools import wraps

# Cargar variables del .env
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")  # ✅ clave para firmar JWT

registro = RegistroUsuario()

# ✅ Función para crear token JWT
def crear_token(email, rol):
    payload = {
        "email": email,
        "rol": rol,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
    return token


# ✅ Decorador para proteger rutas con JWT
def token_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        auth = request.headers.get("Authorization", "")

        # Debe venir así: "Bearer TOKEN"
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Token requerido"}), 401

        token = auth.split(" ")[1]

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            request.user = data  # guardamos email y rol
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        return f(*args, **kwargs)

    return decorador


# ✅ Registro de usuario
@app.route('/registro', methods=['POST'])
def registro_usuario():
    try:
        datos = request.get_json()

        if not datos:
            return jsonify({'error': 'Credenciales Invalidas'}), 400

        email = datos.get('email', '').strip()
        password = datos.get('password', '').strip()

        if not email or not password:
            return jsonify({'error': 'Credenciales Invalidas'}), 400

        resultado = registro.registrar_usuario(email, password)

        if resultado['status']:
            return jsonify({'mensaje': resultado['mensaje']}), resultado['codigo']
        else:
            return jsonify({'error': resultado['mensaje']}), resultado['codigo']

    except Exception:
        return jsonify({'error': 'Error interno del servidor'}), 500


# ✅ Login con JWT
@app.route('/login', methods=['POST'])
def login():
    try:
        datos = request.get_json()

        if not datos:
            return jsonify({"error": "Credenciales inválidas"}), 400

        email = datos.get("email", "").strip()
        password = datos.get("password", "").strip()

        if not email or not password:
            return jsonify({"error": "Credenciales inválidas"}), 400

        # Validar usuario en BD
        resultado = registro.validar_usuario(email, password)

        if not resultado["status"]:
            return jsonify({"error": resultado["mensaje"]}), 401

        # Crear token
        token = crear_token(email, resultado["rol"])

        return jsonify({
            "mensaje": "Login exitoso",
            "token": token
        }), 200

    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


# ✅ Actualizar contraseña
@app.route('/actualizar-password', methods=['PUT'])
def actualizar_password():
    try:
        datos = request.get_json()

        if not datos:
            return jsonify({'error': 'Datos inválidos'}), 400

        email = datos.get('email', '').strip()
        password_actual = datos.get('password_actual', '').strip()
        password_nueva = datos.get('password_nueva', '').strip()

        if not email or not password_actual or not password_nueva:
            return jsonify({'error': 'Datos incompletos'}), 400

        resultado = registro.actualizar_password(email, password_actual, password_nueva)

        if resultado['status']:
            return jsonify({'mensaje': resultado['mensaje']}), resultado['codigo']
        else:
            return jsonify({'error': resultado['mensaje']}), resultado['codigo']

    except Exception:
        return jsonify({'error': 'Error interno del servidor'}), 500


# ✅ Actualizar rol
@app.route('/actualizar-rol', methods=['PUT'])
def actualizar_rol():
    try:
        datos = request.get_json()

        if not datos:
            return jsonify({'error': 'Datos inválidos'}), 400

        email = datos.get('email', '').strip()
        rol = datos.get('rol', '').strip()

        if not email or not rol:
            return jsonify({'error': 'Datos incompletos'}), 400

        resultado = registro.actualizar_rol(email, rol)

        if resultado['status']:
            return jsonify({'mensaje': resultado['mensaje']}), resultado['codigo']
        else:
            return jsonify({'error': resultado['mensaje']}), resultado['codigo']

    except Exception:
        return jsonify({'error': 'Error interno del servidor'}), 500


# ✅ Ruta de salud
@app.route('/salud', methods=['GET'])
def salud():
    return jsonify({'estado': 'El servidor está funcionando correctamente'}), 200


# ✅ Ruta protegida con token
@app.route('/perfil', methods=['GET'])
@token_requerido
def perfil():
    return jsonify({
        "mensaje": "Acceso autorizado",
        "datos_token": request.user
    }), 200



# ✅ Ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)