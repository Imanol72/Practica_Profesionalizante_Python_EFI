# services.py
from repositories.categoria_repository import CategoriaRepository

class CategoriaService:
    def __init__(self):
        self.repository = CategoriaRepository()

    def get_all_categorias(self):
        return self.repository.get_all()

    def get_categoria_by_id(self, categoria_id):
        return self.repository.get_by_id(categoria_id)

    def create_categoria(self, nombre):
        return self.repository.create(nombre)

    def update_categoria(self, categoria_id, nombre):
        return self.repository.update(categoria_id, nombre)

    def delete_categoria(self, categoria_id):
        return self.repository.delete(categoria_id)
