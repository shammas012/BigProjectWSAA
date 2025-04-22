#references
#https://flask.palletsprojects.com/en/latest/patterns/appfactories/
#https://flask-sqlalchemy.palletsprojects.com/en/latest/quickstart/#configuration
#


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

dbEngine = SQLAlchemy()

# def create_app():
#     app = Flask(__name__)

#     app.config.from_pyfile(os.path.join(os.path.dirname(__file__), 'config.py'))

#     print("Config file loaded:", app.config.get('SQLALCHEMY_DATABASE_URI'))

#     print("SQLALCHEMY_DATABASE_URI:", app.config.get('SQLALCHEMY_DATABASE_URI'))
 
#     dbEngine.init_app(app)

#     return app


from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # debug
    #print("SQLALCHEMY_DATABASE_URI:", app.config.get('SQLALCHEMY_DATABASE_URI'))
    dbEngine.init_app(app)

    #move the below routing later to a common routes file..
    @app.route('/')
    def index():
        return "Smart Service Desk is live!"
    return app