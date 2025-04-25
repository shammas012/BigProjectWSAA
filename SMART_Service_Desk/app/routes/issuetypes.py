#references
# https://realpython.com/flask-by-example-part-1-project-setup/
# https://flask.palletsprojects.com/en/stable/api/#flask.json.jsonify
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# https://realpython.com/flask-blueprint/
# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy


from flask import Blueprint, jsonify, request
from app.models import db, IssueType


#########################User##############################

bp = Blueprint('users', __name__, url_prefix='/api')

# decorator / attribute for /api/users GET
@bp.route('/users', methods=['GET'])
def getUserList():
    users = User.query.all()
    return jsonify([user.serializeJson() for user in users])

# decorator / attribute for /api/users POST
@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(
        username=data['username'],
        email=data['email'],
        roleid=data['roleid']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serializeJson()), 200


#####################UserRoles######################################

@bp.route('/roles', methods=['GET'])
def getUserRoles():
    roles = UserRole.query.all()
    return jsonify([r.serialize() for r in roles])

@bp.route('/roles', methods=['POST'])
def createUserRole():
    data = request.get_json()
    role = UserRole(description=data['description'])
    db.session.add(role)
    db.session.commit()
    return jsonify(role.serialize()), 201

# sample request
# {
#   "description": "Customer"
# }
