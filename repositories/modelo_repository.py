# repositories/modelo_repository.py
from models import Modelo
from app import db

class ModeloRepository:

    def crear_modelo(self, data):
        # Suponiendo que 'data' es un diccionario con los datos del modelo
        nuevo_modelo = Modelo(**data)  # Utiliza los datos para crear una nueva instancia
        db.session.add(nuevo_modelo)
        db.session.commit()
        return nuevo_modelo

    def obtener_todos_los_modelos(self):
        return Modelo.query.all()  # Retorna todos los modelos

    def obtener_modelo_por_id(self, modelo_id):
        return Modelo.query.get(modelo_id)  # Retorna un modelo por su ID
