from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField,IntegerField, SubmitField, DecimalField
from wtforms.validators import DataRequired, NumberRange

class AccesorioForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    compatibilidad = BooleanField('Compatibilidad')
    equipo_id = SelectField('Equipo', coerce=int, validators=[DataRequired()])


class EquipoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    categoria = StringField('Categoría', validators=[DataRequired()])
    costo = DecimalField('Costo', validators=[DataRequired(), NumberRange(min=0)])
    modelo_id = SelectField('Modelo', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Crear Equipo')

class ModeloForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    marca_id = SelectField('Marca', coerce=int, validators=[DataRequired()])


class MarcaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    categoria = StringField('Categoría', validators=[DataRequired()])
    submit = SubmitField('Crear Marca')


class StockForm(FlaskForm):
    equipo_id = SelectField('Equipo', coerce=int, validators=[DataRequired()])
    cantidad_disponible = IntegerField('Cantidad Disponible', validators=[DataRequired()])
    cantidad_minima = IntegerField('Cantidad Mínima', validators=[DataRequired()])
    ubicacion_almacen = StringField('Ubicación Almacén', validators=[DataRequired()])


class CategoriaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])

