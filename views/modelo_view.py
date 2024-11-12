from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from forms import ModeloForm
from services.modelo_service import ModeloService
from services.marca_service import MarcaService
from schemas import ModeloSchema

modelo_bp = Blueprint('modelo', __name__)
modelo_service = ModeloService()
modelo_bp = Blueprint('modelo_bp', __name__)

# Crear un nuevo modelo
@modelo_bp.route('/modelos', methods=['POST'])
def crear_modelo():
    data = request.get_json()
    modelo = modelo_service.crear_modelo(data)
    return jsonify({"id": modelo.id, "nombre": modelo.nombre}), 201

# Obtener todos los modelos
@modelo_bp.route('/modelos', methods=['GET'])
def obtener_todos_los_modelos():
    modelos = modelo_service.obtener_todos_los_modelos()
    return jsonify([modelo.nombre for modelo in modelos])  # Devuelve una lista con los nombres de los modelos

# Obtener modelo por ID
@modelo_bp.route('/modelos/<int:modelo_id>', methods=['GET'])
def obtener_modelo(modelo_id):
    modelo = modelo_service.obtener_modelo_por_id(modelo_id)
    if modelo:
        return jsonify({"id": modelo.id, "nombre": modelo.nombre}), 200
    return jsonify({"mensaje": "Modelo no encontrado"}), 404
