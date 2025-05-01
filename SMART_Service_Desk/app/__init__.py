#references
# https://flask.palletsprojects.com/en/latest/patterns/appfactories/
# https://flask-sqlalchemy.palletsprojects.com/en/latest/quickstart/#configuration
# https://stackoverflow.com/questions/14888799/disable-console-messages-in-flask-server
# https://stackoverflow.com/questions/24649789/how-to-force-a-rotating-name-with-pythons-timedrotatingfilehandler
# https://docs.python.org/3/library/logging.html#formatter-objects
# https://flask.palletsprojects.com/en/stable/logging/

from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os, logging
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
    
    #logic for Logging goes here 

    if not os.path.exists('logs'):
        os.mkdir('logs')

    today = datetime.now().strftime('%Y-%m-%d')
    log_file = f'logs/smartsd_{today}.log'  # ✅ your format

    file_handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)

    # register blueprint here
    from app.routes.users import bp as bpUsers
    app.register_blueprint(bpUsers)

    from app.routes.issuetypes import bp as bpIssueTypes
    app.register_blueprint(bpIssueTypes)

    from app.routes.project import bp as bpProjects
    app.register_blueprint(bpProjects)

    from app.routes.tickets import bp as bpTickets
    app.register_blueprint(bpTickets)

    from app.routes.workflows import bp as bpWorkflows
    app.register_blueprint(bpWorkflows)

    from app.routes.ui import bp as bpUi
    app.register_blueprint(bpUi)


    from . import models

    #move the below routing later to a common routes file..
    @app.route('/')
    def index():
        return "Smart Service Desk is live!"
    return app