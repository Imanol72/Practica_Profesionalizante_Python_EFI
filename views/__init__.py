
from .auth_view import auth_bp
from .marca_view import marca_bp
from .modelo_view import modelo_bp
from .stock_view import stock_bp
from .accesorio_view import accesorio_bp
from .categoria_view import categoria_bp
from .equipo_view import equipo_bp
from .main import main_app_bp

def register_blueprint(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(marca_bp)
    app.register_blueprint(modelo_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(accesorio_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(equipo_bp)
    app.register_blueprint(main_app_bp)