from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from forms import CategoriaForm
from services.categoria_services import CategoriaService
from schemas import CategoriaSchema

categoria_bp = Blueprint('categoria_bp', __name__)
categoria_service = CategoriaService()

@categoria_bp.route('/categoria', methods=['GET', 'POST'])
@jwt_required()  # Asegura que el usuario esté autenticado
def manage_categoria():
    additional_info = get_jwt()
    administrador = additional_info.get('administrador')

    if not administrador:  # Verifica si el usuario es administrador
        return jsonify({"Mensaje": "No está autorizado para acceder a esta sección"}), 403

    if request.method == 'GET':
        # Si la solicitud es GET, obtiene todas las categorías
        categorias = categoria_service.get_all_categorias()
        categoria_schema = CategoriaSchema(many=True)
        return jsonify(categoria_schema.dump(categorias))

    elif request.method == 'POST':
        # Si la solicitud es POST, crea una nueva categoría
        data = request.get_json()  # Usa JSON en lugar de request.form

        # Asegúrate de que los datos contienen el campo "nombre"
        if 'nombre' not in data:
            return jsonify({"message": "Nombre is required"}), 400

        # Usar el servicio para crear la categoría
        categoria = categoria_service.create_categoria(data['nombre'])
        categoria_schema = CategoriaSchema()
        return jsonify(categoria_schema.dump(categoria)), 201


@categoria_bp.route('/categoria/<int:id>', methods=['PUT'])
@jwt_required()  # Asegura que el usuario esté autenticado
def update_categoria(id):
    additional_info = get_jwt()
    administrador = additional_info.get('administrador')

    if not administrador:  # Verifica si el usuario es administrador
        return jsonify({"Mensaje": "No está autorizado para acceder a esta sección"}), 403

    # Obtén los datos enviados en formato JSON
    data = request.get_json()

    # Verifica que los datos contengan el campo 'nombre'
    if 'nombre' not in data:
        return jsonify({"message": "El campo 'nombre' es obligatorio"}), 400

    # Llama al servicio para actualizar la categoría
    categoria = categoria_service.update_categoria(id, data['nombre'])
    
    if categoria:
        categoria_schema = CategoriaSchema()
        return jsonify(categoria_schema.dump(categoria)), 200
    
    return jsonify({"message": "Categoria no encontrada"}), 404


@categoria_bp.route('/categoria/<int:id>', methods=['DELETE'])
@jwt_required()  # Asegura que el usuario esté autenticado
def delete_categoria(id):
    additional_info = get_jwt()
    administrador = additional_info.get('administrador')

    if not administrador:  # Verifica si el usuario es administrador
        return jsonify({"Mensaje": "No está autorizado para acceder a esta sección"}), 403

    categoria = categoria_service.delete_categoria(id)
    if categoria:
        return jsonify({"message": "Categoria deleted"}), 200
    return jsonify({"message": "Categoria not found"}), 404

