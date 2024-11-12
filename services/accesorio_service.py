from repositories.accesorio_repository import AccesorioRepository

class AccesorioService:
    def __init__(self):
        self.repository = AccesorioRepository()

    def obtener_todos_los_accesorios(self):
        return self.repository.obtener_todos()

    def crear_accesorio(self, data):
        return self.repository.crear(data)
