from flask import Blueprint, jsonify
from models import Accesorio, Categoria, Equipo, Marca, Modelo, Stock, Tipo, User
from schemas import AccesorioSchema, CategoriaSchema, EquipoSchema, MarcaSchema, ModeloSchema, StockSchema, UserSchema

# Se crea el Blueprint
main_app_bp = Blueprint('main_app_bp', __name__)


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
