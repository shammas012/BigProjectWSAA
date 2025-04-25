#references
# https://realpython.com/flask-by-example-part-1-project-setup/
# https://flask.palletsprojects.com/en/stable/api/#flask.json.jsonify
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# https://realpython.com/flask-blueprint/
# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy


from flask import Blueprint, jsonify, request
from app.models import db, Ticket


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

    # Create the ticket
    ticket = Ticket(
        key=f"",# there should be a logic to generate the key sequentially,
        summary=data['summary'],
        description=data['description'],
        createdBy=data['createdBy'],
        assignedTo=data.get('assignedTo'),
        issueTypeId=data['issueTypeId'],
        statusId=data['statusId'],
        projectId=data['projectId']
    )

    db.session.add(ticket)
    db.session.commit()
    return jsonify(ticket.serializeJson()), 200





