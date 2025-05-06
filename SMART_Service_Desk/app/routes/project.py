#references
# https://realpython.com/flask-by-example-part-1-project-setup/
# https://flask.palletsprojects.com/en/stable/api/#flask.json.jsonify
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# https://realpython.com/flask-blueprint/
# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy


from flask import Blueprint, current_app, jsonify, request
from app.routes.utils import log_exceptions
from app.models import db, Project
from flask_jwt_extended import jwt_required, get_jwt_identity


#########################Project##############################

bp = Blueprint('projects', __name__, url_prefix='/api')

# decorator / attribute for /api/projects GET
@bp.route('/projects', methods=['GET'])
@log_exceptions
@jwt_required()
def getIssueTypeList():
    projects = Project.query.all()
    return jsonify([issuetype.serializeJson() for issuetype in projects])


# decorator / attribute for /api/projects POST
@bp.route('/projects', methods=['POST'])
@log_exceptions
@jwt_required()
def createIssueType():
    try:
        data = request.get_json()
        project = Project(
            name=data['name'],
            shortName=data['shortName'],
            createdBy=data['createdBy']
        )
        db.session.add(project)
        db.session.commit()
        current_app.logger.info(f"Created project {project.description}.")

        return jsonify(project.serializeJson()), 201
    except Exception as ex:
        db.session.rollback()  
        current_app.logger.error(f"Failed to create project: {str(ex)}")
        return jsonify({"error": "Failed to create project"}), 500


