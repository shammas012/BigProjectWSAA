#references
# https://realpython.com/flask-by-example-part-1-project-setup/
# https://flask.palletsprojects.com/en/stable/api/#flask.json.jsonify
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# https://realpython.com/flask-blueprint/
# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy


from flask import Blueprint, jsonify, request
from app.models import db, Ticket, Project


#########################ticket##############################

bp = Blueprint('tickets', __name__, url_prefix='/api')

# decorator / attribute for /api/projects GET
@bp.route('/tickets', methods=['GET'])
def getTicketList():
    tickets = Ticket.query.all()
    return jsonify([ticket.serializeJson() for ticket in tickets])


# decorator / attribute for /api/projects POST
@bp.route('/tickets', methods=['POST'])
def createTicket():
    data = request.get_json()

    project = Project.query.get(data['projectId'])
    if not project:
        return jsonify({"error": "Project dont exist in Smart SD"}), 400

    # Increment ticket number safely
    newTicketNumber = project.lastTicketNumber + 1

    # Create the ticket
    ticket = Ticket(
        key=f"{project.shortName}-{newTicketNumber}",
        summary=data['summary'],
        description=data['description'],
        createdBy=data['createdBy'],
        assignedTo=data.get('assignedTo'),
        issueTypeId=data['issueTypeId'],
        statusId=data['statusId'],
        projectId=data['projectId']
    )
    project.lastTicketNumber = newTicketNumber
    db.session.add(ticket)
    db.session.add(project)
    db.session.commit()
    return jsonify(ticket.serializeJson()), 200





