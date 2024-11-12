from app import db
from datetime import datetime


class Accesorio(db.Model):
    __tablename__ = 'accesorio'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)
    accesorio = db.Column(db.String(100), nullable=False)
    compatibilidad = db.Column(db.Boolean)


class Categoria(db.Model):
    __tablename__ = 'categoria'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)


class Equipo(db.Model):
    __tablename__ = 'equipo'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    costo = db.Column(db.Integer, nullable=False)


class Marca(db.Model):
    __tablename__ = 'marca'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)


class Modelo(db.Model):
    __tablename__ = 'modelo'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=False)


class Stock(db.Model):
    __tablename__ = 'stock'

    id = db.Column(db.Integer, primary_key=True)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)
    cantidad_disponible = db.Column(db.Integer, nullable=False)
    cantidad_minima = db.Column(db.Integer, nullable=False)
    ubicacion_almacen = db.Column(db.String(100), nullable=False)


class Tipo(db.Model):
    __tablename__ = 'tipo'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return self.nombre


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # contraseña hasheada
    is_admin = db.Column(db.Boolean, default=True)

    def __str__(self):
        return self.username
