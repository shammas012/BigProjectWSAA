#references
# https://realpython.com/flask-by-example-part-1-project-setup/
# https://flask.palletsprojects.com/en/stable/api/#flask.json.jsonify
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# https://realpython.com/flask-blueprint/
# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy


from flask import Blueprint, jsonify, request, current_app
from app.models import db, Ticket, Project, WorkflowStatus
from app.routes.utils import log_exceptions


#########################ticket##############################

bp = Blueprint('tickets', __name__, url_prefix='/api')

# decorator / attribute for /api/tickets GET
@bp.route('/tickets', methods=['GET'])
@log_exceptions
def getTicketList():
    tickets = Ticket.query.all()
    return jsonify([ticket.serializeJson() for ticket in tickets])


# decorator / attribute for /api/tickets POST
@bp.route('/tickets', methods=['POST'])
@log_exceptions
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



