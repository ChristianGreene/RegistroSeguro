from flask import Flask, request, jsonify
from registro_logica import RegistroUsuario

app = Flask(__name__)
registro = RegistroUsuario()

@app.route('/registro', methods=['POST'])
def registro_usuario():
    """
    Endpoint POST para registrar un nuevo usuario
    
    Body esperado:
    {
        "email": "usuario@example.com",
        "password": "contraseña"
    }
    """
    try:
        # Obtener datos del request
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                'error': 'Credenciales Invalidas'
            }), 400
        
        email = datos.get('email', '').strip()
        password = datos.get('password', '').strip()
        
        # Validar que los campos existan
        if not email or not password:
            return jsonify({
                'error': 'Credenciales Invalidas'
            }), 400
        
        # Registrar el usuario
        resultado = registro.registrar_usuario(email, password)
        
        # Retornar respuesta según el resultado
        if resultado['status']:
            return jsonify({
                'mensaje': resultado['mensaje']
            }), resultado['codigo']
        else:
            return jsonify({
                'error': resultado['mensaje']
            }), resultado['codigo']
    
    except Exception as e:
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500

@app.route('/salud', methods=['GET'])
def salud():
    """Endpoint de verificación de salud del servidor"""
    return jsonify({
        'estado': 'El servidor está funcionando correctamente'
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
