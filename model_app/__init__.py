import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db = SQLAlchemy()
    db.init_app(app)

    from model_app import db

    @app.cli.command("init_db")
    def init_db():
        db.init_db()

    # blueprint for non-auth parts of app
    from model_app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
