#references
# https://realpython.com/flask-by-example-part-1-project-setup/
# https://flask.palletsprojects.com/en/stable/api/#flask.json.jsonify
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# https://realpython.com/flask-blueprint/
# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy


from flask import Blueprint, jsonify, request
from app.models import db, IssueType


#########################User##############################

bp = Blueprint('issue_types', __name__, url_prefix='/api')

# decorator / attribute for /api/users GET
@bp.route('/issuetypes', methods=['GET'])
def getIssueTypeList():
    issue_types = IssueType.query.all()
    return jsonify([issuetype.serializeJson() for issuetype in issue_types])


# decorator / attribute for /api/issuetypes POST
@bp.route('/issuetypes', methods=['POST'])
def createIssueType():
    data = request.get_json()
    issueType = IssueType(
        description=data['description']
    )
    db.session.add(issueType)
    db.session.commit()
    return jsonify(issueType.serializeJson()), 200


