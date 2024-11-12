from app import ma
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from models import Stock, Equipo, Modelo, Marca, Accesorio, User, Categoria


class AccesorioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Accesorio

    id = ma.auto_field(dump_only=True)
    nombre = ma.auto_field(required=True)
    compatibilidad = ma.auto_field()  
    equipo_id = ma.auto_field(required=True)


class EquipoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Equipo

    id = ma.auto_field(dump_only=True)
    nombre = ma.auto_field(required=True)
    categoria = ma.auto_field(required=True)
    costo = ma.auto_field()  


class ModeloSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Modelo 

    id = ma.auto_field(dump_only=True)
    nombre = ma.auto_field()  
    marca_id = ma.auto_field()  


class MarcaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Marca

    id = ma.auto_field(dump_only=True)
    nombre = ma.auto_field(required=True)
    categoria = ma.auto_field()  


class StockSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Stock  

    equipo_id = ma.auto_field()
    cantidad_minima = ma.auto_field()


class CategoriaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Categoria  

    id = ma.auto_field(dump_only=True)
    nombre = ma.auto_field(required=True)

class StockSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Stock  

    id = ma.auto_field(dump_only=True)
    equipo_id = ma.auto_field(required=True)
    cantidad_disponible = ma.auto_field(required=True)
    cantidad_minima = ma.auto_field(required=True)
    ubicacion_almacen = ma.auto_field(required=True)

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()   
    is_admin = ma.auto_field()
    password_hash = ma.auto_field()


class MinimalUserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    username = ma.auto_field()



class StockSchema(SQLAlchemySchema):
    class Meta:
        model = Stock
        load_instance = True

    id = auto_field()
    equipo_id = auto_field()
    cantidad_disponible = auto_field()
    cantidad_minima = auto_field()
    ubicacion_almacen = auto_field()



