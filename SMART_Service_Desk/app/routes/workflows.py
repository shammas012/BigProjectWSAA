#references
# https://realpython.com/flask-by-example-part-1-project-setup/
# https://flask.palletsprojects.com/en/stable/api/#flask.json.jsonify
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# https://realpython.com/flask-blueprint/
# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy


from flask import Blueprint, jsonify, request
from app.models import db, WorkflowStatus,WorkflowTransition


#########################statuses##############################

bp = Blueprint('workflows', __name__, url_prefix='/api')

# decorator / attribute for /api/statuses GET
@bp.route('/statuses', methods=['GET'])
def getWorkflowStatuses():
    statuses = WorkflowStatus.query.all()
    return jsonify([status.serializeJson() for status in statuses])

# decorator / attribute for /api/statuses POST
@bp.route('/statuses', methods=['POST'])
def createWorkflowStatus():
    data = request.get_json()
    status = WorkflowStatus(
        description=data['description'],
        is_default=data.get('is_default', False),
        is_terminal=data.get('is_terminal', False)
    )
    db.session.add(status)
    db.session.commit()
    return jsonify(status.serializeJson()), 201

# {
#   "description": "Open",
#   "is_default": true,
#   "is_terminal": false
# }

#####################Transitions######################################

@bp.route('/transitions', methods=['GET'])
def getWorkflowTransitions():
    transitions = WorkflowTransition.query.all()
    return jsonify([transition.serializeJson() for transition in transitions])

@bp.route('/transitions', methods=['POST'])
def createWorkflowTransition():
    data = request.get_json()
    transition = WorkflowTransition(
        fromStatus=data['fromStatus'],
        toStatus=data['toStatus']
    )
    db.session.add(transition)
    db.session.commit()
    return jsonify(transition.serializeJson()), 201

