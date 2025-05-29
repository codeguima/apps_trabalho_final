from flask import Flask # type: ignore
from .extensions import db, cache
from .routes import bp
from .db_utils import create_tables

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    cache.init_app(app)

    app.register_blueprint(bp)

    # Garante criação das tabelas após o db estar disponível
    with app.app_context():
        create_tables(app)

    return app
