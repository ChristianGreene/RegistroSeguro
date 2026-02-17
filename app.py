from flask import Flask, request, jsonify
from registro_logica import RegistroUsuario

app = Flask(__name__)
registro = RegistroUsuario()

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


# ✅ NUEVO: Actualizar contraseña
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


# ✅ NUEVO: Actualizar rol
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


@app.route('/salud', methods=['GET'])
def salud():
    return jsonify({'estado': 'El servidor está funcionando correctamente'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
