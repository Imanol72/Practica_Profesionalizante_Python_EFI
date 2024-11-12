from app import db
from models import Stock

class StockRepository:

    def obtener_todo_el_stock(self):
        return Stock.query.all()

    def crear_stock(self, data):
        stock = Stock(
            equipo_id=data['equipo_id'],
            cantidad_disponible=data['cantidad_disponible'],
            cantidad_minima=data['cantidad_minima'],
            ubicacion_almacen=data['ubicacion_almacen']
        )
        db.session.add(stock)
        db.session.commit()
        return stock
