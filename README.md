# Practica_Profesionalizante_Python_EFI

Trabajo Final para la materia de prácticas profecionalizantes en python en segundo año de la carrera de Desarrollo en Software en el Instituto Tecnológico de Rio Cuarto

Este trabajo consiste en desarrollar una API que permita realizar un login en una aplicacion de venta de celulares. Esta API debe solicitar el logueo del usuario para poder acceder a la información de la aplicacion, como tambien poder distinguir entre usuarios comunes y adeministradores.

Los usuarios comunes solo podran acceder a las vistas de lo que está cargado en la aplicacion mientras que los adminitradores podran tener acceso a un CRUD que les permita crear leer actualizar y borrar los campos de la aplicacion como crear leer actualizar y borrar nuevos usuarios.

## Características de la Aplicación

- **Autenticación JWT**: Los usuarios deben autenticarse para acceder a las vistas de la aplicación. La autenticación se realiza mediante **JSON Web Tokens (JWT)**.
  
- **Roles de Usuario**: Existen dos tipos de usuarios:
  - **Usuarios Comunes**: Solo pueden visualizar la información cargada en la aplicación (productos, marcas, modelos, etc.).
  - **Administradores**: Tienen permisos para crear, leer, actualizar y eliminar registros dentro de la aplicación, incluyendo la gestión de usuarios.

- **Funcionalidades de la API**:
  - **Marcas**: Los administradores pueden gestionar las marcas de los productos.
  - **Modelos**: Los administradores pueden gestionar los modelos de los productos.
  - **Stock**: Los administradores pueden gestionar el stock de los productos, incluyendo el registro de equipos y la cantidad disponible.
  - **Usuarios**: Los administradores pueden crear, editar y eliminar usuarios, así como asignarles roles.

## Estructura del Proyecto

La aplicación se basa en una arquitectura **Flask** que implementa una serie de rutas para las diferentes funcionalidades de la API. Estas rutas están protegidas por autenticación JWT para garantizar que solo los usuarios autorizados puedan acceder a ciertos recursos.

- **Rutas de la API**:
  - `/login`: Ruta para autenticar al usuario y obtener un token JWT.
  - `/marca`: Ruta para gestionar las marcas de los productos.
  - `/modelo`: Ruta para gestionar los modelos de los productos.
  - `/stock`: Ruta para gestionar el stock de los productos.

- **Servicios**:
  - `MarcaService`: Gestiona las operaciones relacionadas con las marcas.
  - `ModeloService`: Gestiona las operaciones relacionadas con los modelos.
  - `StockService`: Gestiona las operaciones relacionadas con el stock.

- **Schemas**:
  - `MarcaSchema`: Utilizado para serializar y deserializar los datos de las marcas.
  - `ModeloSchema`: Utilizado para serializar y deserializar los datos de los modelos.
  - `StockSchema`: Utilizado para serializar y deserializar los datos del stock.

## Instalación

Para instalar y ejecutar la aplicación, sigue estos pasos:

### Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Un entorno virtual (opcional, pero recomendado)

### Pasos de instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu_usuario/Practica_Profesionalizante_Python_EFI.git
   cd Practica_Profesionalizante_Python_EFI

    Crea un entorno virtual (opcional):

python3 -m venv venv
source venv/bin/activate  # En sistemas Unix
.\venv\Scripts\activate  # En Windows

Instala las dependencias:

pip install -r requirements.txt

Configura las variables de entorno:

    Crea un archivo .env en la raíz del proyecto y agrega las siguientes variables:

    FLASK_APP=app.py
    FLASK_ENV=development
    SECRET_KEY=tu_clave_secreta
    JWT_SECRET_KEY=tu_clave_secreta_jwt

Inicia la base de datos: Si es necesario, realiza las migraciones de la base de datos para crear las tablas:

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

Ejecuta la aplicación:

    flask run

    La aplicación estará disponible en http://localhost:5000.

Uso de la API
Autenticación

Para acceder a las rutas protegidas, los usuarios deben autenticar su sesión mediante el endpoint /login. Esto devolverá un token JWT que debe ser incluido en el encabezado Authorization de las solicitudes.
Ejemplo de login:

POST /login
Content-Type: application/json

{
  "username": "usuario",
  "password": "contraseña"
}

Respuesta:

{
  "access_token": "token_jwt_aqui"
}

El token debe ser enviado en el encabezado de las solicitudes siguientes:

Authorization: Bearer token_jwt_aqui

Rutas Disponibles
GET /marca

Obtiene una lista de todas las marcas disponibles. Solo accesible para administradores.
POST /marca

Crea una nueva marca. Solo accesible para administradores.
GET /modelo

Obtiene una lista de todos los modelos disponibles. Solo accesible para administradores.
POST /modelo

Crea un nuevo modelo. Solo accesible para administradores.
GET /stock

Obtiene la lista de stock disponible. Solo accesible para administradores.
POST /restar_stock

Crea o actualiza un registro de stock. Solo accesible para administradores.