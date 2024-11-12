from repositories.marca_repository import MarcaRepository
from schemas import MarcaSchema

class MarcaService:

    def __init__(self):
        self.marca_repository = MarcaRepository()
        self.marca_schema = MarcaSchema()

    def obtener_todas_las_marcas(self):
        marcas = self.marca_repository.obtener_todas_las_marcas()
        return self.marca_schema.dump(marcas, many=True)
    

    def crear_marca(self, data):
        nueva_marca = self.marca_repository.crear_marca(data['nombre'], data['categoria'])
        return self.marca_schema.dump(nueva_marca)
