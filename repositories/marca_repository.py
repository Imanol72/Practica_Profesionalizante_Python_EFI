from app import db
from models import Marca

class MarcaRepository:
    
    def obtener_todas_las_marcas(self):
        return Marca.query.all()

    def crear_marca(self, nombre, categoria):
        nueva_marca = Marca(nombre=nombre, categoria=categoria)
        db.session.add(nueva_marca)
        db.session.commit()
        return nueva_marca
