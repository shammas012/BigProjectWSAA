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

from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from SMART_Service_Desk.config import Config

load_dotenv()

db = SQLAlchemy()
migrate = Migrate() # Added to fix db init issues
jwt = JWTManager()  # <--- This is the missing piece

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['ENV'] = 'development'
    app.config.from_object(Config)
    # debug
    #print("SQLALCHEMY_DATABASE_URI:", app.config.get('SQLALCHEMY_DATABASE_URI'))
    db.init_app(app)
    jwt.init_app(app)
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
    from SMART_Service_Desk.app.routes.users import bp as bpUsers
    app.register_blueprint(bpUsers)

    from SMART_Service_Desk.app.routes.issuetypes import bp as bpIssueTypes
    app.register_blueprint(bpIssueTypes)

    from SMART_Service_Desk.app.routes.project import bp as bpProjects
    app.register_blueprint(bpProjects)

    from SMART_Service_Desk.app.routes.tickets import bp as bpTickets
    app.register_blueprint(bpTickets)

    from SMART_Service_Desk.app.routes.workflows import bp as bpWorkflows
    app.register_blueprint(bpWorkflows)

    from SMART_Service_Desk.app.routes.ui import bp as bpUi
    app.register_blueprint(bpUi)

    from SMART_Service_Desk.app.routes.auth import bp as bpAuth
    app.register_blueprint(bpAuth)

    @app.context_processor
    def enable_user():
        from flask_jwt_extended import get_jwt_identity
        from SMART_Service_Desk.app.models import User
        try:
            user_id = get_jwt_identity()
            user = db.session.get(User, user_id)
            return dict(current_user=user)
        except Exception:
            return dict(current_user=None)

    from . import models

    #move the below routing later to a common routes file..
    @app.route('/')
    def index():
        return "Smart Service Desk is live!"
    return app