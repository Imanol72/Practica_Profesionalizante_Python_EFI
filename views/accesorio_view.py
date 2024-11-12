from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from services.accesorio_service import AccesorioService
from services.equipo_service import EquipoService
from forms import AccesorioForm
from schemas import AccesorioSchema

accesorio_bp = Blueprint('accesorio', __name__)

@accesorio_bp.route('/accesorios', methods=['GET', 'POST'])
@jwt_required()  # Este decorador asegura que el usuario esté autenticado
def listar_accesorios():
    # Verifica el JWT del usuario
    additional_info = get_jwt()
    administrador = additional_info.get('administrador')

    if not administrador:  
        return jsonify({"Mensaje": "No está autorizado para acceder a esta sección"}), 403

    accesorio_service = AccesorioService()
    equipo_service = EquipoService()
    form = AccesorioForm()
    form.equipo_id.choices = [(e.id, e.nombre) for e in equipo_service.obtener_todos_los_equipos()]

    # Si la solicitud es POST y el formulario es válido
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

    # Si la solicitud es GET, muestra los accesorios
    if request.method == 'GET':
        accesorios = accesorio_service.obtener_todos_los_accesorios()
        
        if not accesorios:  # Si no hay accesorios, devuelve una lista vacía
            return jsonify({'accesorios': []})
        
        accesorio_schema = AccesorioSchema(many=True)
        return jsonify(accesorios=accesorio_schema.dump(accesorios))

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

    accesorios = accesorio_service.obtener_todos_los_accesorios()
    accesorio_schema = AccesorioSchema(many=True)
    return jsonify(accesorios=accesorio_schema.dump(accesorios))
