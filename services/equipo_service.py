# services/equipo_service.py
from repositories.equipo_repository import EquipoRepository

class EquipoService:
    def __init__(self):
        self.repositorio = EquipoRepository()

    def obtener_todos(self):
        return self.repositorio.obtener_todos()

    def crear_equipo(self, data):
        return self.repositorio.crear_equipo(data)
