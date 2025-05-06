#references
# https://realpython.com/flask-by-example-part-1-project-setup/
# https://flask.palletsprojects.com/en/stable/api/#flask.json.jsonify
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# https://realpython.com/flask-blueprint/
# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy
# https://stackoverflow.com/questions/75578445/flask-error-or-404-query-resulting-in-sql-error
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods/PUT


from datetime import datetime
from flask import Blueprint, jsonify, request, current_app
from app.models import TicketHistory, db, Ticket, Project, WorkflowStatus
from app.routes.utils import log_exceptions
from flask_jwt_extended import jwt_required, get_jwt_identity

#########################ticket##############################

bp = Blueprint('tickets', __name__, url_prefix='/api')

# decorator / attribute for /api/tickets GET
@bp.route('/tickets', methods=['GET'])
@jwt_required()
@log_exceptions
def getTicketList():
    tickets = Ticket.query.all()
    return jsonify([ticket.serializeJson() for ticket in tickets])


# decorator / attribute for /api/tickets POST
@bp.route('/tickets', methods=['POST'])
@log_exceptions
@jwt_required()
def createTicket():
    try:
        data = request.get_json()

        project = Project.query.get(data['projectId'])
        if not project:
            return jsonify({"error": "Project dont exist in Smart SD"}), 400
        
        #Value "None" should appear in the UI dropdown, if UI no default status set.
        #In Phase two the status might need to be tagged against each project, rather than using same statuses/worflows for all projects
        default_status = WorkflowStatus.query.filter_by(is_default=True).first()
        if not default_status:
            return jsonify({"error": "Default workflow status not set at the moment"}), 400

        # Increment ticket number sequentially
        newTicketNumber = project.lastTicketNumber + 1

        # Create the ticket
        ticket = Ticket(
            key=f"{project.shortName}-{newTicketNumber}",
            summary=data['summary'],
            description=data['description'],
            createdBy=data['createdBy'],
            assignedTo=data.get('assignedTo') or None, # to avoid error when empty string is passed as assignee ID.
            issueTypeId=data['issueTypeId'],
            statusId=default_status.id,
            projectId=data['projectId']
        )
        project.lastTicketNumber = newTicketNumber
        db.session.add(ticket)
        db.session.add(project)
        db.session.commit()

        current_app.logger.info(f"Created ticket {ticket.key} in project {project.name}")

        return jsonify(ticket.serializeJson()), 201
    
    except Exception as ex:
        db.session.rollback()  
        current_app.logger.error(f"Failed to create ticket: {str(ex)}")
        return jsonify({"error": "Failed to create ticket"}), 500

# post crud body
# {
#   "summary": "Shammas unable to access smart DB database",
#   "description": "Shammas unable to access smart DB database, credentials not working",
#   "createdBy": "9174ae62-6288-429e-b1f2-eda1ae7907f7",
#   "assignedTo": "", 
#   "issueTypeId": "dd65eef8-ddcf-4a4c-9e74-f4778f01a4cd",
#   "projectId": "f748c0a2-545e-4c17-a452-80cb2f7c28fe"
# }

# GET /api/tickets/<key>
@bp.route('/tickets/<key>', methods=['GET'])
@log_exceptions
@jwt_required()
def getTicketByKey(key):
    try:
        ticket = Ticket.query.get_or_404(key)
        return jsonify({
            'key': ticket.key,
            'summary': ticket.summary,
            'description': ticket.description,
            'createdBy': ticket.createdBy,
            'assignedTo': ticket.assignedTo,
            'issueTypeId': ticket.issueTypeId,
            'statusId': ticket.statusId,
            'projectId': ticket.projectId,
            'createdAt': ticket.createdAt,
            'updatedAt': ticket.updatedAt
        })
    except Exception as ex:
            current_app.logger.error(f"Unable to fetch ticket {ticket.key} details: {str(ex)}")
            return jsonify({"error": "Unable to fetch ticket details for {ticket.key}"}), 500

# PUT /api/tickets/<key>
@bp.route('/tickets/<key>', methods=['PUT'])
@log_exceptions
@jwt_required()
def updateTicket(key):
    try:
        ticket = Ticket.query.get_or_404(key)
        data = request.get_json()

        changed = False  # Track if anything changed compared to the ticket details already existing in DB
        oldStatusId = ticket.statusId

        if 'summary' in data and data['summary'] != ticket.summary:
            ticket.summary = data['summary']
            changed = True

        if 'description' in data and data['description'] != ticket.description:
            ticket.description = data['description']
            changed = True

        if 'assignedTo' in data and data['assignedTo'] != ticket.assignedTo:
            ticket.assignedTo = data['assignedTo']
            changed = True

        if 'statusId' in data and data['statusId'] != ticket.statusId:
            ticket.statusId = data['statusId']
            changed = True

        if 'issueTypeId' in data and data['issueTypeId'] != ticket.issueTypeId:
            ticket.issueTypeId = data['issueTypeId']
            changed = True

        if changed:
            ticket.updatedAt = datetime.utcnow()
            db.session.commit()
            current_app.logger.info(f"Details updated for ticket {ticket.key}.")
            updateHistoryDetails(ticket, oldStatusId)
            return jsonify({"message": "Ticket updated", "ticket": ticket.key}), 200
        else:
            current_app.logger.info(f"Ticket {ticket.key} not updated : No changes detected.")
            return jsonify({"message": "No changes detected."}), 200           
    except Exception as ex:
        db.session.rollback()  
        current_app.logger.error(f"Failed to update ticket {Ticket.key} : {str(ex)}")
        return jsonify({"error": "Failed to update ticket {Ticket.key}"}), 500

def updateHistoryDetails(ticket, oldStatusId):
    historyDetails = TicketHistory(
                ticketKey=ticket.key,
                fromStatus=oldStatusId,
                toStatus=ticket.statusId,
                changedBy="9439d2de-8aeb-45e8-a496-27d4f9dd9c60", # hardcoded for now, will be passed by UI, for API calls to get current user details implement authentication
                timestamp=datetime.utcnow()
            )
    db.session.add(historyDetails)
    current_app.logger.info(f"Ticket {ticket.key} status changed from {historyDetails.fromStatus} to {historyDetails.toStatus} by user {historyDetails.changedBy}")
    
# PUT request body
# {
#   "summary": "Shammas unable to access smart DB database",
#   "description": "Shammas unable to access smart DB database, credentials not working",
#   "assignedTo": "", 
#   "issueTypeId": "dd65eef8-ddcf-4a4c-9e74-f4778f01a4cd",
#   "statusId": "b1b2c3d4-5678-4321-9101-abcdef123456"

#  }
    




