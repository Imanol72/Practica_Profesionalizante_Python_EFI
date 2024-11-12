# repository.py
from models import Categoria
from app import db

class CategoriaRepository:
    def __init__(self):
        pass

    def get_all(self):
        return Categoria.query.all()

    def get_by_id(self, categoria_id):
        return Categoria.query.get(categoria_id)

    def create(self, nombre):
        categoria = Categoria(nombre=nombre)
        db.session.add(categoria)
        db.session.commit()
        return categoria

    def update(self, categoria_id, nombre):
        categoria = Categoria.query.get(categoria_id)
        if categoria:
            categoria.nombre = nombre
            db.session.commit()
        return categoria

    def delete(self, categoria_id):
        categoria = Categoria.query.get(categoria_id)
        if categoria:
            db.session.delete(categoria)
            db.session.commit()
        return categoria
