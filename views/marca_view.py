from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from forms import MarcaForm
from services.marca_service import MarcaService

marca_bp = Blueprint('marca', __name__)

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
