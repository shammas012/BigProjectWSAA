#references
#https://flask.palletsprojects.com/en/latest/patterns/appfactories/
#https://flask-sqlalchemy.palletsprojects.com/en/latest/quickstart/#configuration
#


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from .config import Config


db = SQLAlchemy()
migrate = Migrate() # Added to fix db init issues

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # debug
    #print("SQLALCHEMY_DATABASE_URI:", app.config.get('SQLALCHEMY_DATABASE_URI'))
    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.users import bp as bpUsers
    app.register_blueprint(bpUsers)


    from . import models

    #move the below routing later to a common routes file..
    @app.route('/')
    def index():
        return "Smart Service Desk is live!"
    return app