from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from forms import StockForm
from services.stock_service import StockService
from services.equipo_service import EquipoService
from schemas import StockSchema

stock_bp = Blueprint('stock', __name__)

# Instancia del esquema de stock
stock_schema = StockSchema()
stocks_schema = StockSchema(many=True)

@stock_bp.route('/stock', methods=['GET'])
@jwt_required()  # Este decorador asegura que el usuario esté autenticado para el método GET
def listar_stock():
    additional_info = get_jwt()  # Obtiene el JWT del usuario
    administrador = additional_info.get('administrador')

    if not administrador:
        return jsonify({"Mensaje": "No está autorizado para acceder a esta sección"}), 403

    stocks = StockService.obtener_todo_el_stock()
    return jsonify(stocks_schema.dump(stocks)), 200


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
