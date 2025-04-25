#references
# https://realpython.com/flask-by-example-part-1-project-setup/
# https://flask.palletsprojects.com/en/stable/api/#flask.json.jsonify
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# https://realpython.com/flask-blueprint/
# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy


from flask import Blueprint, jsonify, request
from app.models import db, Project


#########################IssueType##############################

bp = Blueprint('projects', __name__, url_prefix='/api')

# decorator / attribute for /api/projects GET
@bp.route('/projects', methods=['GET'])
def getIssueTypeList():
    projects = Project.query.all()
    return jsonify([issuetype.serializeJson() for issuetype in projects])


# decorator / attribute for /api/projects POST
@bp.route('/projects', methods=['POST'])
def createIssueType():
    data = request.get_json()
    project = Project(
        description=data['description']
    )
    db.session.add(project)
    db.session.commit()
    return jsonify(project.serializeJson()), 200


