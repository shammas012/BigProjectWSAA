#references
# https://realpython.com/flask-by-example-part-1-project-setup/
# https://flask.palletsprojects.com/en/stable/api/#flask.json.jsonify
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# https://realpython.com/flask-blueprint/
# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy
# https://flask.palletsprojects.com/en/latest/logging/
# https://docs.sqlalchemy.org/en/20/orm/session_basics.html


from flask import Blueprint, jsonify, request, current_app
from app.models import db, User, UserRole
from app.routes.utils import log_exceptions


#########################User##############################

bp = Blueprint('users', __name__, url_prefix='/api')

# decorator / attribute for /api/users GET
@bp.route('/users', methods=['GET'])

@log_exceptions
def getUserList():
    users = User.query.all()
    return jsonify([user.serializeJson() for user in users])

# decorator / attribute for /api/users POST
@bp.route('/users', methods=['POST'])
@log_exceptions
def createUser():
    try:
        data = request.get_json()
        user = User(
            username=data['username'],
            email=data['email'],
            roleid=data['roleid'],
            fullname=data['fullname'],
        )
        db.session.add(user)
        db.session.commit()
        return jsonify(user.serializeJson()), 201
    
    except Exception as ex:
        db.session.rollback()  
        current_app.logger.error(f"Failed to create user: {str(ex)}")
        return jsonify({"error": "Failed to create user"}), 500
# {
#   "fullname" : "Nuwaylah ZS",
#   "username": "NuwaylahS",
#   "email": "Nuwaylah@smartsd.com",
#   "roleid": "03c2cee8-a00a-41d3-a3e5-0ae0fd728f58"
# }


#####################UserRoles######################################

@bp.route('/roles', methods=['GET'])
@log_exceptions
def getUserRoles():
    roles = UserRole.query.all()
    return jsonify([r.serialize() for r in roles])

@bp.route('/roles', methods=['POST'])
@log_exceptions
def createUserRole():
    try:
        data = request.get_json()
        role = UserRole(description=data['description'])
        db.session.add(role)
        db.session.commit()
        return jsonify(role.serialize()), 201
    
    except Exception as ex:
        db.session.rollback() 
        current_app.logger.error(f"Failed to create user: {str(ex)}")
        return jsonify({"error": "Failed to create user"}), 500
    
# sample request
# {
#   "description": "Customer"
# }
