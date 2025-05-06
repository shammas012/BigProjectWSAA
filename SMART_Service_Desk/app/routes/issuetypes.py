#references
# https://realpython.com/flask-by-example-part-1-project-setup/
# https://flask.palletsprojects.com/en/stable/api/#flask.json.jsonify
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# https://realpython.com/flask-blueprint/
# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy


from flask import Blueprint, current_app, jsonify, request
from app.routes.utils import log_exceptions
from app.models import db, IssueType
from flask_jwt_extended import jwt_required, get_jwt_identity


#########################IssueType##############################

bp = Blueprint('issue_types', __name__, url_prefix='/api')

# decorator / attribute for /api/issuetypes GET
@bp.route('/issuetypes', methods=['GET'])
@log_exceptions
@jwt_required()
def getIssueTypeList():
    issue_types = IssueType.query.all()
    return jsonify([issuetype.serializeJson() for issuetype in issue_types])


# decorator / attribute for /api/issuetypes POST
@bp.route('/issuetypes', methods=['POST'])
@log_exceptions
@jwt_required()
def createIssueType():
    try:
        data = request.get_json()
        issueType = IssueType(
            description=data['description']
        )
        db.session.add(issueType)
        db.session.commit()

        current_app.logger.info(f"Created issuetype {issueType.description}.")
        
        return jsonify(issueType.serializeJson()), 201
    except Exception as ex:
        db.session.rollback()  
        current_app.logger.error(f"Failed to create issue type: {str(ex)}")
        return jsonify({"error": "Failed to create issue type"}), 500

# {
#   "description": "Incident"
# }
