# API Segura de Registro de Usuarios

Esta es una API REST segura para el registro de usuarios con contraseñas hasheadas usando bcrypt.

## Características

- ✅ Validación de credenciales (email y password)
- ✅ Constraseña debe tener entre 8-10 caracteres
- ✅ Verificación de usuarios duplicados
- ✅ Hash de contraseñas con bcrypt
- ✅ Base de datos SQLite3
- ✅ Respuestas HTTP estándar

## Requisitos

- Python 3.7+
- pip

## Instalación

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

2. Crear la base de datos (ejecutar una sola vez):
```bash
python init_db.py
```

## Uso

1. Iniciar el servidor:
```bash
python app.py
```

El servidor estará disponible en `http://localhost:5000`

2. Registrar un usuario:
```bash
curl -X POST http://localhost:5000/registro \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "password": "mipass123"
  }'
```

## Endpoints

### POST /registro

Registra un nuevo usuario.

**Request:**
```json
{
  "email": "usuario@example.com",
  "password": "mipass123"
}
```

**Respuestas:**

- **201 Created**: Usuario registrado exitosamente
```json
{
  "mensaje": "Usuario Registrado"
}
```

- **400 Bad Request**: Credenciales inválidas
```json
{
  "error": "Credenciales Invalidas"
}
```

- **409 Conflict**: Usuario ya existe
```json
{
  "error": "El usuario ya existe"
}
```

- **500 Internal Server Error**: Error en el servidor
```json
{
  "error": "Error interno del servidor"
}
```

### GET /salud

Verifica que el servidor esté funcionando.

**Response:**
```json
{
  "estado": "El servidor está funcionando correctamente"
}
```

## Estructura de la Base de Datos

```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'cliente'
)
```

## Seguridad

- Las contraseñas se hashean con bcrypt usando 12 rounds
- Se valida la longitud de la contraseña (8-10 caracteres)
- Se previene SQL injection usando prepared statements
- Se verifica la unicidad del email antes de registrar
