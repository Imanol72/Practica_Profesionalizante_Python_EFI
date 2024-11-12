from app import db
from models import Accesorio

class AccesorioRepository:
    def __init__(self):
        self.model = Accesorio

    def obtener_todos(self):
        return self.model.query.all()

    def crear(self, data):
        nuevo_accesorio = self.model(
            nombre=data['nombre'],
            compatibilidad=data['compatibilidad'],
            equipo_id=data['equipo_id']
        )
        db.session.add(nuevo_accesorio)
        db.session.commit()
        return nuevo_accesorio
