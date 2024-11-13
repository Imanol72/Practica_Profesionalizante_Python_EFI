Documentación del Archivo auth_view.py
Importaciones y Configuración

import os
from datetime import timedelta

from app import db 
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from models import User
from schemas import UserSchema, MinimalUserSchema

    Objetivo: Importa las bibliotecas necesarias, incluyendo las de seguridad, JWT para manejo de tokens y Flask para las solicitudes.
    BluePrint: auth_bp se define como un blueprint para encapsular las rutas de autenticación.

Rutas
1. Ruta de Login (/login)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.authorization
    username = data.username
    password = data.password

    usuario = User.query.filter_by(username=username).first()
    
    if usuario and check_password_hash(
        pwhash=usuario.password_hash, password=password
    ):
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=40),
            additional_claims=dict(
            administrador=usuario.is_admin
            )
        )
        return jsonify({'Token':f'Bearer {access_token}'})

    return jsonify(Mensaje="El usuario y la contraseña al parecer no coinciden")

    Descripción: Verifica las credenciales de usuario y genera un token JWT si son correctas.
    Flujo:
        Extrae username y password de la solicitud.
        Comprueba el username en la base de datos.
        Si existe y la contraseña es válida, genera un token JWT que expira en 40 minutos.
        El token incluye un campo administrador para manejar permisos de usuario.
        Si falla la autenticación, se devuelve un mensaje de error.

2. Crear y Listar Usuarios (/users)

@auth_bp.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        is_admin = data.get('is_admin')

    try:
        nuevo_usuario = User(
            username=username,
            password_hash=generate_password_hash(password),
            is_admin=is_admin,
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify(
            {
            "Mensaje": "Usuario creado correctamente",
            "Usuario": UserSchema().dump(obj=nuevo_usuario)
            }
            )
    except:
            return jsonify(
                {
                "Mensaje": "Fallo la creación del nuevo usuario",
                }
            )
    
    usuarios = User.query.all()
    return UserSchema().dump(obj=usuarios, many=True)

    POST: Crea un usuario nuevo.
        Campos Requeridos: username, password, is_admin.
        Proceso: Genera el hash de la contraseña, guarda el usuario en la base de datos y retorna un mensaje de éxito.
        Manejo de Errores: Si falla, devuelve un mensaje de error.
    GET: Lista todos los usuarios.

3. Eliminar Usuario (/users/<int:id>/delete)

@auth_bp.route('/users/<int:id>/delete', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if not administrador:
        return jsonify({"Mensaje": "Solo el admin puede eliminar usuarios"}), 403

    usuario = User.query.get(id)
    if not usuario:
        return jsonify({"Mensaje": "Usuario no encontrado"}), 404

    try:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"Mensaje": "Usuario eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"Mensaje": "Fallo al eliminar el usuario", "Error": str(e)}), 500

    Descripción: Permite que solo los administradores eliminen usuarios.
    Verificación de Autorización: Comprueba el token JWT para verificar si el usuario tiene permisos de administrador.
    Errores: Maneja si el usuario no existe o falla el proceso de eliminación.

4. Actualizar Usuario (/users/<int:id>/update)

@auth_bp.route('/users/<int:id>/update', methods=['PUT'])
@jwt_required()
def update_user(id):
    additional_data = get_jwt()
    administrador = additional_data.get('administrador')

    if administrador is not True:
        return jsonify({"Mensaje": "No tienes permiso para actualizar usuarios"}), 403

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    is_admin = data.get('is_admin')

    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"Mensaje": "Usuario no encontrado"}), 404

        user.username = username if username else user.username
        user.password_hash = generate_password_hash(password) if password else user.password_hash
        user.is_admin = is_admin if is_admin is not None else user.is_admin

        db.session.commit()
        return jsonify({"Mensaje": "Usuario actualizado correctamente", "Usuario": user.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"Mensaje": "Error al actualizar el usuario: " + str(e)}), 500

    Descripción: Permite que un administrador actualice los detalles de un usuario.
    Verificación de Autorización: Requiere un token con permisos de administrador.
    Actualización Condicional: Solo se actualizan los campos proporcionados en el cuerpo de la solicitud.
    Manejo de Errores: Se devuelve un mensaje de error detallado en caso de fallo.

Resumen

Este archivo auth_view.py proporciona funcionalidad de autenticación y administración de usuarios, gestionando tanto la creación, actualización, y eliminación de usuarios, como la verificación de permisos.
Tú dijiste:
Necesito que lo documentes
ChatGPT Plus
ChatGPT

Aquí tienes la documentación en formato Markdown para tu archivo auth_view.py, explicando cada sección y ruta con sus funcionalidades:

# Documentación de `auth_view.py`

Este archivo define las rutas y funcionalidades relacionadas con la autenticación y administración de usuarios en la aplicación. Incluye rutas para el inicio de sesión (`login`), la creación y listado de usuarios, y operaciones de administración como la actualización y eliminación de usuarios, con controles de permisos para administradores.

## Importaciones y Configuración

```python
import os
from datetime import timedelta

from app import db 
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from models import User
from schemas import UserSchema, MinimalUserSchema

    Descripción: Estas importaciones incluyen:
        generate_password_hash y check_password_hash para gestionar contraseñas.
        create_access_token y jwt_required de flask_jwt_extended para crear tokens de autenticación y proteger rutas.
    Blueprint: Se crea un Blueprint llamado auth_bp, que encapsula las rutas de autenticación.

Rutas
Ruta de Login (/login)

@auth_bp.route('/login', methods=['POST'])
def login():
    ...

    Descripción: Autentica a un usuario mediante username y password.
    Entrada: Credenciales (username y password) enviadas en el encabezado de autorización de la solicitud.
    Salida: Si la autenticación es correcta, se devuelve un token JWT con un tiempo de expiración de 40 minutos. El token incluye un campo administrador que indica si el usuario tiene permisos de administrador.
    Errores: Si las credenciales no coinciden, se devuelve un mensaje de error.

Ejemplo de Solicitud:

POST /login
Authorization: Basic <base64(username:password)>

Ejemplo de Respuesta:

{
    "Token": "Bearer <JWT_TOKEN>"
}

Ruta para Crear y Listar Usuarios (/users)

@auth_bp.route('/users', methods=['GET', 'POST'])
def users():
    ...

    POST: Crea un usuario nuevo.
        Entrada: JSON con username, password, y is_admin para indicar si el usuario tiene rol de administrador.
        Salida: Mensaje de éxito y datos del usuario creado.
        Errores: Si falla la creación, se devuelve un mensaje de error.

    Ejemplo de Solicitud:

POST /users
Content-Type: application/json
{
    "username": "nuevo_usuario",
    "password": "contraseña_segura",
    "is_admin": false
}

Ejemplo de Respuesta (Éxito):

{
    "Mensaje": "Usuario creado correctamente",
    "Usuario": {
        "id": 1,
        "username": "nuevo_usuario",
        "is_admin": false
    }
}

GET: Devuelve una lista de todos los usuarios.

Ejemplo de Solicitud:

GET /users

Ejemplo de Respuesta:

    [
        {
            "id": 1,
            "username": "admin",
            "is_admin": true
        },
        {
            "id": 2,
            "username": "nuevo_usuario",
            "is_admin": false
        }
    ]

Ruta para Eliminar Usuarios (/users/<int:id>/delete)

@auth_bp.route('/users/<int:id>/delete', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    ...

    Descripción: Permite que los usuarios con rol de administrador eliminen usuarios específicos.
    Entrada: id del usuario a eliminar (pasado en la URL).
    Permisos: Solo los administradores pueden eliminar usuarios.
    Salida: Mensaje de éxito si la eliminación es correcta, o mensajes de error en caso de fallos.

Ejemplo de Solicitud:

DELETE /users/2/delete
Authorization: Bearer <JWT_TOKEN>

Ejemplo de Respuesta (Éxito):

{
    "Mensaje": "Usuario eliminado correctamente"
}

Ruta para Actualizar Usuarios (/users/<int:id>/update)

@auth_bp.route('/users/<int:id>/update', methods=['PUT'])
@jwt_required()
def update_user(id):
    ...

    Descripción: Permite que un administrador actualice los datos de un usuario específico.
    Entrada: id del usuario en la URL y JSON opcional con username, password, y/o is_admin.
    Permisos: Solo los administradores pueden actualizar usuarios.
    Salida: Mensaje de éxito y datos del usuario actualizado, o mensajes de error en caso de fallos.

Ejemplo de Solicitud:

PUT /users/1/update
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
{
    "username": "admin_actualizado",
    "password": "nueva_contraseña",
    "is_admin": true
}

Ejemplo de Respuesta (Éxito):

{
    "Mensaje": "Usuario actualizado correctamente",
    "Usuario": {
        "id": 1,
        "username": "admin_actualizado",
        "is_admin": true
    }
}

# Documentación de `categoria_view.py`

Este archivo define las rutas y funcionalidades relacionadas con la administración de categorías en la aplicación. Incluye rutas para listar, crear, actualizar y eliminar categorías. Estas operaciones están protegidas mediante autenticación, y solo los usuarios con permisos de administrador pueden acceder a ellas.

## Importaciones y Configuración

```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from forms import CategoriaForm
from services.categoria_services import CategoriaService
from schemas import CategoriaSchema

    Descripción: Estas importaciones incluyen:
        jwt_required y get_jwt de flask_jwt_extended para proteger las rutas y obtener datos adicionales del token JWT.
        CategoriaService y CategoriaSchema para interactuar con la lógica de negocio y serializar los datos de la categoría.
    Blueprint: Se crea un Blueprint llamado categoria_bp para agrupar las rutas de categorías.
    Servicio: CategoriaService se instancia como categoria_service para facilitar las operaciones de CRUD en categorías.

Rutas
Ruta para Administrar Categorías (/categoria)

@categoria_bp.route('/categoria', methods=['GET', 'POST'])
@jwt_required()
def manage_categoria():
    ...

    Descripción: Permite listar todas las categorías (GET) o crear una nueva categoría (POST). Solo accesible para usuarios administradores.
    Entrada:
        GET: No requiere parámetros.
        POST: JSON con el campo nombre para crear una nueva categoría.
    Salida:
        GET: Lista de todas las categorías.
        POST: Datos de la categoría creada en caso de éxito.
    Errores: Si el usuario no es administrador, se devuelve un error 403. Si falta el campo nombre en una solicitud POST, se devuelve un error 400.

Ejemplo de Solicitud (GET):

GET /categoria
Authorization: Bearer <JWT_TOKEN>

Ejemplo de Respuesta (GET):

[
    {
        "id": 1,
        "nombre": "Electrónica"
    },
    {
        "id": 2,
        "nombre": "Juguetería"
    }
]

Ejemplo de Solicitud (POST):

POST /categoria
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
{
    "nombre": "Ropa"
}

Ejemplo de Respuesta (POST):

{
    "id": 3,
    "nombre": "Ropa"
}

Ruta para Actualizar una Categoría (/categoria/<int:id>)

@categoria_bp.route('/categoria/<int:id>', methods=['PUT'])
@jwt_required()
def update_categoria(id):
    ...

    Descripción: Actualiza el nombre de una categoría existente, identificado por id. Solo accesible para usuarios administradores.
    Entrada: id de la categoría en la URL y JSON con el campo nombre.
    Salida: Datos de la categoría actualizada si la operación es exitosa.
    Errores: Si el usuario no es administrador, se devuelve un error 403. Si falta el campo nombre, se devuelve un error 400. Si no se encuentra la categoría, se devuelve un error 404.

Ejemplo de Solicitud:

PUT /categoria/1
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
{
    "nombre": "Electrodomésticos"
}

Ejemplo de Respuesta:

{
    "id": 1,
    "nombre": "Electrodomésticos"
}

Ruta para Eliminar una Categoría (/categoria/<int:id>)

@categoria_bp.route('/categoria/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_categoria(id):
    ...

    Descripción: Elimina una categoría existente, identificado por id. Solo accesible para usuarios administradores.
    Entrada: id de la categoría a eliminar en la URL.
    Salida: Mensaje confirmando la eliminación en caso de éxito.
    Errores: Si el usuario no es administrador, se devuelve un error 403. Si no se encuentra la categoría, se devuelve un error 404.

Ejemplo de Solicitud:

DELETE /categoria/1
Authorization: Bearer <JWT_TOKEN>

Ejemplo de Respuesta (Éxito):

{
    "message": "Categoria deleted"
}

# Documentación de `accesorio_view.py`

Este archivo define las rutas y funcionalidades para gestionar accesorios en la aplicación. Incluye las operaciones para listar y crear nuevos accesorios. Las rutas están protegidas mediante autenticación JWT, y solo los usuarios con permisos de administrador pueden acceder a estas funcionalidades.

## Importaciones y Configuración

```python
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from services.accesorio_service import AccesorioService
from services.equipo_service import EquipoService
from forms import AccesorioForm
from schemas import AccesorioSchema

    Descripción: Importa:
        jwt_required y get_jwt de flask_jwt_extended para proteger las rutas y obtener datos adicionales del token JWT.
        AccesorioService y EquipoService para interactuar con la lógica de negocio de accesorios y equipos.
        AccesorioForm para validar los datos al crear un accesorio.
        AccesorioSchema para serializar los datos de los accesorios.
    Blueprint: Se crea un Blueprint llamado accesorio_bp para agrupar las rutas de accesorios.

Rutas
Ruta para Listar y Crear Accesorios (/accesorios)

@accesorio_bp.route('/accesorios', methods=['GET', 'POST'])
@jwt_required()
def listar_accesorios():
    ...

    Descripción: Esta ruta permite dos operaciones:
        GET: Lista todos los accesorios.
        POST: Crea un nuevo accesorio en el sistema.
    Protección: Ambas operaciones están protegidas mediante JWT y solo accesibles para usuarios administradores.
    Servicios: Utiliza AccesorioService para gestionar los accesorios y EquipoService para obtener equipos compatibles.

Verificación de Administrador

additional_info = get_jwt()
administrador = additional_info.get('administrador')
if not administrador:
    return jsonify({"Mensaje": "No está autorizado para acceder a esta sección"}), 403

    Descripción: Extrae el campo administrador del token JWT. Si el usuario no es administrador, devuelve un mensaje de error con código 403, indicando que no tiene permiso.

GET: Listar Accesorios

if request.method == 'GET':
    accesorios = accesorio_service.obtener_todos_los_accesorios()
    if not accesorios:
        return jsonify({'accesorios': []})
    accesorio_schema = AccesorioSchema(many=True)
    return jsonify(accesorios=accesorio_schema.dump(accesorios))

    Descripción: Si la solicitud es GET, se listan todos los accesorios disponibles.
    Salida: Devuelve una lista de accesorios en formato JSON. Si no hay accesorios, devuelve una lista vacía.

Ejemplo de Solicitud (GET):

GET /accesorios
Authorization: Bearer <JWT_TOKEN>

Ejemplo de Respuesta (GET):

{
    "accesorios": [
        {
            "id": 1,
            "nombre": "Cargador",
            "compatibilidad": "Universal",
            "equipo_id": 2
        },
        {
            "id": 2,
            "nombre": "Cable USB",
            "compatibilidad": "USB-C",
            "equipo_id": 3
        }
    ]
}

POST: Crear un Accesorio

if request.method == 'POST' and form.validate_on_submit():
    data = {
        'nombre': form.nombre.data,
        'compatibilidad': form.compatibilidad.data,
        'equipo_id': form.equipo_id.data
    }
    accesorio = accesorio_service.crear_accesorio(data)
    accesorio_schema = AccesorioSchema()
    return jsonify({
        'message': 'Accesorio creado exitosamente',
        'accesorio': accesorio_schema.dump(accesorio)
    }), 201

    Descripción: Si la solicitud es POST, crea un nuevo accesorio utilizando los datos proporcionados y validados por AccesorioForm.
    Entrada: JSON con los siguientes campos:
        nombre: Nombre del accesorio.
        compatibilidad: Compatibilidad del accesorio.
        equipo_id: ID del equipo compatible.
    Salida: Devuelve un mensaje de éxito y los datos del accesorio creado en caso de éxito.

Ejemplo de Solicitud (POST):

POST /accesorios
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
{
    "nombre": "Auriculares Bluetooth",
    "compatibilidad": "Bluetooth 5.0",
    "equipo_id": 1
}

Ejemplo de Respuesta (POST):

{
    "message": "Accesorio creado exitosamente",
    "accesorio": {
        "id": 3,
        "nombre": "Auriculares Bluetooth",
        "compatibilidad": "Bluetooth 5.0",
        "equipo_id": 1
    }
}

# Documentación de `equipo_view.py`

Este archivo define las rutas y funcionalidades para gestionar equipos en la aplicación. Incluye la operación para listar y crear nuevos equipos. La lista de modelos se carga dinámicamente para la selección en el formulario.

## Importaciones y Configuración

```python
from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from forms import EquipoForm
from services.equipo_service import EquipoService
from services.modelo_service import ModeloService

    Descripción:
        Blueprint se usa para definir rutas específicas para los equipos.
        EquipoForm es el formulario para validar y capturar datos de un equipo.
        EquipoService y ModeloService gestionan la lógica de negocio de equipos y modelos respectivamente.
    Blueprint: Se crea un Blueprint llamado equipo_bp para agrupar las rutas de equipo.

Rutas
Ruta para Listar y Crear Equipos (/equipos)

@equipo_bp.route('/equipos', methods=['GET'])
def listar_equipos():
    ...

    Descripción: Esta ruta permite dos operaciones:
        GET: Lista todos los equipos.
        Formulario de creación: Permite crear un nuevo equipo usando los datos proporcionados en el formulario EquipoForm.
    Servicios: Utiliza EquipoService para gestionar los equipos y ModeloService para obtener modelos disponibles.

Poblar el Campo de Selección con Modelos

form.modelo_id.choices = [(m.id, m.nombre) for m in modelo_service.obtener_todos_los_modelos()]

    Descripción: Se obtiene la lista de modelos disponibles a través de ModeloService y se configura como opciones para el campo de selección modelo_id en el formulario.

Procesar el Formulario para Crear un Nuevo Equipo

if form.validate_on_submit():
    data = {
        'nombre': form.nombre.data,
        'categoria': form.categoria.data,
        'costo': form.costo.data,
        'modelo_id': form.modelo_id.data,
    }
    equipo_service.crear_equipo(data)
    return redirect(url_for('equipo.listar_equipos'))

    Descripción: Si el formulario es válido, se crean los datos del equipo con el servicio EquipoService.
    Redirección: Tras la creación exitosa del equipo, se redirige al usuario de nuevo a la página de listado de equipos.

GET: Listar Equipos

equipos = equipo_service.obtener_todos()
equipos_json = [{'id': e.id, 'nombre': e.nombre, 'categoria': e.categoria, 'costo': float(e.costo)} for e in equipos]
return jsonify(equipos=equipos_json)

    Descripción: Obtiene todos los equipos mediante EquipoService y devuelve los datos en formato JSON.
    Formato de Salida: Cada equipo incluye id, nombre, categoria, y costo.

Ejemplo de Solicitud (GET):

GET /equipos

Ejemplo de Respuesta (GET):

{
    "equipos": [
        {
            "id": 1,
            "nombre": "Laptop",
            "categoria": "Computación",
            "costo": 1200.50
        },
        {
            "id": 2,
            "nombre": "Tablet",
            "categoria": "Electrónica",
            "costo": 300.00
        }
    ]
}

# Documentación de `main_view.py`

Este archivo contiene la definición de una ruta para obtener todos los datos de las entidades principales del sistema, como accesorios, categorías, equipos, marcas, modelos, stocks y usuarios. Los datos se devuelven en formato JSON utilizando los esquemas correspondientes para cada entidad.

## Importaciones y Configuración

```python
from flask import Blueprint, jsonify
from models import Accesorio, Categoria, Equipo, Marca, Modelo, Stock, Tipo, User
from schemas import AccesorioSchema, CategoriaSchema, EquipoSchema, MarcaSchema, ModeloSchema, StockSchema, UserSchema

    Descripción:
        Blueprint se usa para organizar las rutas de la aplicación.
        Se importan los modelos de datos (Accesorio, Categoria, Equipo, Marca, Modelo, Stock, User) para realizar consultas a la base de datos.
        Se importan los esquemas correspondientes (AccesorioSchema, CategoriaSchema, EquipoSchema, etc.) para serializar los resultados de las consultas a JSON.

Ruta para Obtener Todos los Datos (/main/data)

@main_app_bp.route('/main/data', methods=['GET'])
def get_all_data():
    accesorios = Accesorio.query.all()
    categorias = Categoria.query.all()
    equipos = Equipo.query.all()
    marcas = Marca.query.all()
    modelos = Modelo.query.all()
    stocks = Stock.query.all()
    users = User.query.all()

    accesorio_schema = AccesorioSchema(many=True)
    categoria_schema = CategoriaSchema(many=True)
    equipo_schema = EquipoSchema(many=True)
    marca_schema = MarcaSchema(many=True)
    modelo_schema = ModeloSchema(many=True)
    stock_schema = StockSchema(many=True)
    user_schema = UserSchema(many=True)

    data = {
        "accesorios": accesorio_schema.dump(accesorios),
        "categorias": categoria_schema.dump(categorias),
        "equipos": equipo_schema.dump(equipos),
        "marcas": marca_schema.dump(marcas),
        "modelos": modelo_schema.dump(modelos),
        "stocks": stock_schema.dump(stocks),
        "usuarios": user_schema.dump(users)
    }

    return jsonify(data)

    Descripción:
        Esta ruta se encarga de obtener los datos de todas las entidades principales del sistema: accesorios, categorías, equipos, marcas, modelos, stocks y usuarios.
        GET: Realiza consultas a la base de datos para obtener todos los registros de las entidades.
        Cada conjunto de datos se serializa utilizando su correspondiente esquema y luego se organiza en un diccionario llamado data.
        Finalmente, los datos son devueltos como respuesta en formato JSON utilizando jsonify.

Respuesta JSON

La respuesta es un objeto JSON que contiene los datos de todas las entidades. La estructura de la respuesta es la siguiente:

{
    "accesorios": [
        { ... },
        { ... }
    ],
    "categorias": [
        { ... },
        { ... }
    ],
    "equipos": [
        { ... },
        { ... }
    ],
    "marcas": [
        { ... },
        { ... }
    ],
    "modelos": [
        { ... },
        { ... }
    ],
    "stocks": [
        { ... },
        { ... }
    ],
    "usuarios": [
        { ... },
        { ... }
    ]
}

Ejemplo de respuesta para accesorios:

{
    "accesorios": [
        {
            "id": 1,
            "nombre": "Cargador",
            "compatibilidad": "iPhone",
            "equipo_id": 1
        },
        {
            "id": 2,
            "nombre": "Auriculares",
            "compatibilidad": "Android",
            "equipo_id": 2
        }
    ]
}

Ejemplo de respuesta para equipos:

{
    "equipos": [
        {
            "id": 1,
            "nombre": "Laptop",
            "categoria": "Computación",
            "costo": 1200.50
        },
        {
            "id": 2,
            "nombre": "Tablet",
            "categoria": "Electrónica",
            "costo": 300.00
        }
    ]
}

# Documentación de `marca_view.py`

Este archivo contiene la definición de una ruta para listar todas las marcas y crear una nueva marca en el sistema. La ruta está protegida por autenticación JWT, asegurando que solo los administradores puedan acceder a estas funcionalidades.

## Importaciones y Configuración

```python
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from forms import MarcaForm
from services.marca_service import MarcaService

    Descripción:
        Blueprint se usa para organizar las rutas de la aplicación.
        jwt_required y get_jwt de flask_jwt_extended se usan para gestionar la autenticación JWT.
        Se importa el formulario MarcaForm para la creación de nuevas marcas.
        Se importa el servicio MarcaService para manejar las operaciones relacionadas con las marcas.

Ruta para Listar y Crear Marcas (/marca)

@marca_bp.route('/marca', methods=['GET', 'POST'])
@jwt_required()  
def listar_marcas():
    additional_info = get_jwt() 
    administrador = additional_info.get('administrador')

    if not administrador:  
        return jsonify({"Mensaje": "No está autorizado para acceder a esta sección"}), 403

    form = MarcaForm()
    
    if form.validate_on_submit():  
        data = {
            'nombre': form.nombre.data,
            'categoria': form.categoria.data,
        }
        marca_service = MarcaService()
        nueva_marca = marca_service.crear_marca(data)  
        return jsonify({"mensaje": "Marca creada exitosamente", "marca": nueva_marca}), 201

    marca_service = MarcaService()
    marcas = marca_service.obtener_todas_las_marcas()
    return render_template('marca_list.html', form=form, marcas=marcas)

    Descripción:
        La ruta /marca maneja tanto solicitudes GET como POST.
        GET: Muestra un formulario para crear una nueva marca y lista todas las marcas existentes.
        POST: Cuando se envía el formulario para crear una nueva marca, se valida el formulario y si es válido, se crea una nueva marca a través del servicio MarcaService. Después de crearla, se devuelve un mensaje de éxito junto con los datos de la nueva marca en formato JSON.
        Autenticación: El decorador @jwt_required() asegura que el usuario esté autenticado. Además, solo los administradores pueden acceder a esta ruta, ya que se verifica el atributo administrador en el JWT.

Respuesta en Caso de Éxito

Cuando una nueva marca es creada con éxito, la respuesta es un objeto JSON con el mensaje de éxito y los datos de la marca creada:

{
    "mensaje": "Marca creada exitosamente",
    "marca": {
        "id": 1,
        "nombre": "Nueva Marca",
        "categoria": "Electrónica"
    }
}

Vista HTML para Listar Marcas

En el caso de una solicitud GET, la ruta renderiza la plantilla marca_list.html, pasando el formulario y la lista de marcas. Esto permite que el usuario vea las marcas existentes y tenga la opción de agregar nuevas.
Ejemplo de datos de marcas mostrados:

{
    "marcas": [
        {
            "id": 1,
            "nombre": "Marca A",
            "categoria": "Electrónica"
        },
        {
            "id": 2,
            "nombre": "Marca B",
            "categoria": "Electrodomésticos"
        }
    ]
}

Seguridad y Acceso

    Autenticación JWT: La ruta está protegida por autenticación JWT, lo que significa que el acceso a la misma está restringido a los usuarios autenticados.
    Autorización: Solo los usuarios que tienen el atributo administrador establecido en su JWT pueden acceder a esta ruta. Si el usuario no es un administrador, se devuelve una respuesta con un código de estado HTTP 403 y un mensaje indicando que no está autorizado para acceder a la sección.

# Documentación de `modelo_view.py`

Este archivo define varias rutas relacionadas con la gestión de modelos en el sistema. Las rutas permiten crear nuevos modelos, obtener todos los modelos existentes y obtener un modelo específico por su ID. Las rutas están protegidas por autenticación JWT cuando es necesario.

## Importaciones y Configuración

```python
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from forms import ModeloForm
from services.modelo_service import ModeloService
from services.marca_service import MarcaService
from schemas import ModeloSchema

    Descripción:
        Blueprint: Se utiliza para definir las rutas relacionadas con el manejo de modelos.
        jwt_required y get_jwt: Son utilizados para asegurar que las rutas están protegidas por autenticación JWT.
        ModeloForm: Se importa el formulario para la creación de modelos (aunque no se utiliza en este archivo).
        ModeloService y MarcaService: Servicios que gestionan la lógica de negocio relacionada con los modelos y las marcas.
        ModeloSchema: Esquema utilizado para serializar los datos de los modelos.

Rutas Definidas
1. Crear un Nuevo Modelo (/modelos)

@modelo_bp.route('/modelos', methods=['POST'])
def crear_modelo():
    data = request.get_json()
    modelo = modelo_service.crear_modelo(data)
    return jsonify({"id": modelo.id, "nombre": modelo.nombre}), 201

    Método: POST

    Descripción:
        Esta ruta recibe datos en formato JSON para crear un nuevo modelo.
        El servicio ModeloService es el encargado de crear el modelo con los datos proporcionados.
        Al crear el modelo, se devuelve un objeto JSON con el ID y el nombre del nuevo modelo.
        El código de respuesta HTTP es 201 para indicar que el recurso fue creado exitosamente.

    Ejemplo de solicitud:

{
    "nombre": "Modelo X",
    "marca_id": 1
}

Ejemplo de respuesta:

    {
        "id": 1,
        "nombre": "Modelo X"
    }

2. Obtener Todos los Modelos (/modelos)

@modelo_bp.route('/modelos', methods=['GET'])
def obtener_todos_los_modelos():
    modelos = modelo_service.obtener_todos_los_modelos()
    return jsonify([modelo.nombre for modelo in modelos])  # Devuelve una lista con los nombres de los modelos

    Método: GET
    Descripción:
        Esta ruta devuelve una lista con los nombres de todos los modelos registrados en el sistema.
        Utiliza el servicio ModeloService para obtener todos los modelos, y luego devuelve solo los nombres de los modelos en una lista.
    Ejemplo de respuesta:

    ["Modelo X", "Modelo Y", "Modelo Z"]

3. Obtener un Modelo Específico por ID (/modelos/<int:modelo_id>)

@modelo_bp.route('/modelos/<int:modelo_id>', methods=['GET'])
def obtener_modelo(modelo_id):
    modelo = modelo_service.obtener_modelo_por_id(modelo_id)
    if modelo:
        return jsonify({"id": modelo.id, "nombre": modelo.nombre}), 200
    return jsonify({"mensaje": "Modelo no encontrado"}), 404

    Método: GET

    Descripción:
        Esta ruta permite obtener un modelo específico a partir de su ID.
        Si el modelo existe, devuelve un objeto JSON con el ID y el nombre del modelo.
        Si el modelo no se encuentra, devuelve un mensaje de error con el código de estado HTTP 404.

    Ejemplo de solicitud:
        Solicitar un modelo con ID 1:

GET /modelos/1

Ejemplo de respuesta (si el modelo existe):

{
    "id": 1,
    "nombre": "Modelo X"
}

Ejemplo de respuesta (si el modelo no existe):

{
    "mensaje": "Modelo no encontrado"
}

# Documentación de `stock_view.py`

Este archivo define las rutas relacionadas con la gestión del stock de equipos en el sistema. Incluye rutas para listar todo el stock y para crear entradas en el stock. Las rutas están protegidas por autenticación JWT para garantizar que solo los usuarios autorizados puedan acceder a ellas.

## Importaciones y Configuración

```python
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from forms import StockForm
from services.stock_service import StockService
from services.equipo_service import EquipoService
from schemas import StockSchema

    Descripción:
        Blueprint: Utilizado para definir las rutas relacionadas con el manejo de stock.
        jwt_required y get_jwt: Usados para asegurarse de que las rutas están protegidas por autenticación JWT.
        StockForm: Formulario utilizado para la creación de registros de stock.
        StockService y EquipoService: Servicios encargados de la lógica de negocio para gestionar el stock y los equipos, respectivamente.
        StockSchema: Esquema utilizado para serializar los datos de stock.

Rutas Definidas
1. Listar el Stock Disponible (/stock)

@stock_bp.route('/stock', methods=['GET'])
@jwt_required()  # Este decorador asegura que el usuario esté autenticado para el método GET
def listar_stock():
    additional_info = get_jwt()  # Obtiene el JWT del usuario
    administrador = additional_info.get('administrador')

    if not administrador:
        return jsonify({"Mensaje": "No está autorizado para acceder a esta sección"}), 403

    stocks = StockService.obtener_todo_el_stock()
    return jsonify(stocks_schema.dump(stocks)), 200

    Método: GET
    Descripción:
        Esta ruta devuelve toda la información sobre el stock disponible.
        Solo los usuarios autenticados con el rol de administrador pueden acceder a esta ruta. Si el usuario no tiene permisos de administrador, se devuelve un mensaje de error con el código HTTP 403.
        Utiliza el servicio StockService para obtener todos los registros de stock y el esquema StockSchema para serializar los datos.
    Ejemplo de respuesta:

    [
        {
            "id": 1,
            "equipo_id": 2,
            "cantidad_disponible": 15,
            "cantidad_minima": 5,
            "ubicacion_almacen": "Almacén A"
        },
        {
            "id": 2,
            "equipo_id": 3,
            "cantidad_disponible": 8,
            "cantidad_minima": 3,
            "ubicacion_almacen": "Almacén B"
        }
    ]

2. Crear o Restar Stock (/restar_stock)

@stock_bp.route('/restar_stock', methods=['POST'])
@jwt_required()  # Este decorador asegura que el usuario esté autenticado para el método POST
def crear_stock():
    additional_info = get_jwt()  # Obtiene el JWT del usuario
    administrador = additional_info.get('administrador')

    if not administrador:
        return jsonify({"Mensaje": "No está autorizado para acceder a esta sección"}), 403

    form = StockForm()
    form.equipo_id.choices = [(e.id, e.nombre) for e in EquipoService.obtener_todos_los_equipos()]

    if form.validate_on_submit():
        data = {
            'equipo_id': form.equipo_id.data,
            'cantidad_disponible': form.cantidad_disponible.data,
            'cantidad_minima': form.cantidad_minima.data,
            'ubicacion_almacen': form.ubicacion_almacen.data
        }
        stock = StockService.crear_stock(data)
        return jsonify(stock_schema.dump(stock)), 201

    return jsonify({"error": "Formulario inválido", "messages": form.errors}), 400

    Método: POST

    Descripción:
        Esta ruta permite la creación de registros de stock, o la actualización de la cantidad disponible de un equipo.
        Solo los usuarios autenticados con el rol de administrador pueden acceder a esta ruta. Si el usuario no tiene permisos de administrador, se devuelve un mensaje de error con el código HTTP 403.
        El formulario StockForm es utilizado para ingresar los detalles del stock, incluyendo el equipo al que pertenece, la cantidad disponible, la cantidad mínima y la ubicación del almacén.
        Si el formulario es válido, se crea un nuevo registro de stock utilizando el servicio StockService.
        Si el formulario no es válido, se devuelve un mensaje de error con los detalles de los problemas del formulario.

    Ejemplo de solicitud:

{
    "equipo_id": 2,
    "cantidad_disponible": 20,
    "cantidad_minima": 5,
    "ubicacion_almacen": "Almacén C"
}

Ejemplo de respuesta (si el stock es creado exitosamente):

{
    "id": 3,
    "equipo_id": 2,
    "cantidad_disponible": 20,
    "cantidad_minima": 5,
    "ubicacion_almacen": "Almacén C"
}

Ejemplo de respuesta (si el formulario es inválido):

{
    "error": "Formulario inválido",
    "messages": {
        "cantidad_disponible": ["Este campo es obligatorio."]
    }
}
