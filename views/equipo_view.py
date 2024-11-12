# views/equipo_view.py
from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from forms import EquipoForm
from services.equipo_service import EquipoService
from services.modelo_service import ModeloService

equipo_bp = Blueprint('equipo', __name__)

@equipo_bp.route('/equipos', methods=['GET', 'POST'])
def listar_equipos():
    form = EquipoForm()
    modelo_service = ModeloService()
    equipo_service = EquipoService()

    # Poblar el campo de selección con modelos
    form.modelo_id.choices = [(m.id, m.nombre) for m in modelo_service.obtener_todos_los_modelos()]

    # Procesar el formulario al enviar
    if form.validate_on_submit():
        data = {
            'nombre': form.nombre.data,
            'categoria': form.categoria.data,
            'costo': form.costo.data,
            'modelo_id': form.modelo_id.data,
        }
        equipo_service.crear_equipo(data)
        return redirect(url_for('equipo.listar_equipos'))

    # Obtener y serializar equipos para retornar como JSON
    equipos = equipo_service.obtener_todos()
    equipos_json = [{'id': e.id, 'nombre': e.nombre, 'categoria': e.categoria, 'costo': float(e.costo)} for e in equipos]
    return jsonify(equipos=equipos_json)
