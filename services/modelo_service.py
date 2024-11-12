from repositories.modelo_repository import ModeloRepository

class ModeloService:

    def __init__(self):
        self.modelo_repository = ModeloRepository()

    def crear_modelo(self, data):
        return self.modelo_repository.crear_modelo(data)

    def obtener_todos_los_modelos(self):
        return self.modelo_repository.obtener_todos_los_modelos()  # Devuelve una lista de objetos modelo

    def obtener_modelo_por_id(self, modelo_id):
        return self.modelo_repository.obtener_modelo_por_id(modelo_id)
