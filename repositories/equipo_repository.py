# repositories/equipo_repository.py
from models import Equipo
from app import db

class EquipoRepository:
    @staticmethod
    def obtener_todos():
        return Equipo.query.all()

    @staticmethod
    def crear_equipo(data):
        nuevo_equipo = Equipo(**data)
        db.session.add(nuevo_equipo)
        db.session.commit()
        return nuevo_equipo
