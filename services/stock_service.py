from models import Stock
from app import db

class StockService:
    def __init__(self):
        pass

    def obtener_todo_el_stock(self):
        return Stock.query.all()

    def obtener_stock_por_id(self, stock_id):
        return Stock.query.get(stock_id)

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

    def actualizar_stock(self, stock_id, data):
        stock = self.obtener_stock_por_id(stock_id)
        if stock:
            stock.equipo_id = data.get('equipo_id', stock.equipo_id)
            stock.cantidad_disponible = data.get('cantidad_disponible', stock.cantidad_disponible)
            stock.cantidad_minima = data.get('cantidad_minima', stock.cantidad_minima)
            stock.ubicacion_almacen = data.get('ubicacion_almacen', stock.ubicacion_almacen)
            db.session.commit()
        return stock

    def eliminar_stock(self, stock_id):
        stock = self.obtener_stock_por_id(stock_id)
        if stock:
            db.session.delete(stock)
            db.session.commit()
        return stock
