from flask import Flask
from config import Config
from app.categorias import categorias
from app.categorias import routes as categorias_routes
from app.anuncios import anuncios
from app.anuncios import routes as anuncios_routes

from app.extensions import db, login_manager


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)

    from app.models import Usuario, Categoria, Anuncio

    from app.main.routes import main

    from app.auth import auth
    from app.auth import routes

    from app.usuarios import usuarios
    from app.usuarios import routes as usuarios_routes

    app.register_blueprint(main)

    app.register_blueprint(auth)

    app.register_blueprint(usuarios)
    app.register_blueprint(categorias)
    app.register_blueprint(anuncios)

    return app