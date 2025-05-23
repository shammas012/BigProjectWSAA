#references
# https://realpython.com/flask-by-example-part-1-project-setup/
# https://flask.palletsprojects.com/en/stable/api/#flask.json.jsonify
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# https://realpython.com/flask-blueprint/
# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy
# https://flask.palletsprojects.com/en/latest/logging/
# https://docs.sqlalchemy.org/en/20/orm/session_basics.html


from flask import Blueprint, jsonify, request, current_app
from SMART_Service_Desk.app.models import db, User, UserRole
from SMART_Service_Desk.app.routes.utils import log_exceptions
from flask_jwt_extended import jwt_required, get_jwt_identity

#########################User##############################

bp = Blueprint('users', __name__, url_prefix='/api')

# decorator / attribute for /api/users GET
@bp.route('/users', methods=['GET'])
@jwt_required()
@log_exceptions
def getUserList():
    users = User.query.all()
    return jsonify([user.serializeJson() for user in users])

# decorator / attribute for /api/users POST
@bp.route('/users', methods=['POST'])
@log_exceptions
@jwt_required()
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
        current_app.logger.info(f"Created user {user.username}.")

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


# decorator / attribute for /api/users/<user_id> PUT
@bp.route('/users/<user_id>', methods=['PUT'])
@log_exceptions
@jwt_required()
def updateUser(user_id):
    try:
        print(f"PUT /users/{user_id} was called")
        data = request.get_json()
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Update fields if provided in request
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.fullname = data.get('fullname', user.fullname)
        user.roleid = data.get('roleid', user.roleid)

        db.session.commit()
        current_app.logger.info(f"Updated user {user.username}.")

        return jsonify(user.serializeJson()), 200

    except Exception as ex:
        db.session.rollback()
        current_app.logger.error(f"Failed to update user: {str(ex)}")
        return jsonify({"error": "Failed to update user"}), 500

{
  "email": "Nuwaylah@smartsd.com",
  "fullname": "Nuwaylah Zaisha",
  "roleid": "03c2cee8-a00a-41d3-a3e5-0ae0fd728f58",
  "username": "NuwaylahS"
}


#####################UserRoles######################################

@bp.route('/roles', methods=['GET'])
@log_exceptions
@jwt_required()
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
        current_app.logger.info(f"Created user role {role.description}.")

        return jsonify(role.serialize()), 201
    
    except Exception as ex:
        db.session.rollback() 
        current_app.logger.error(f"Failed to create user: {str(ex)}")
        return jsonify({"error": "Failed to create user"}), 500
    
# sample request
# {
#   "description": "Customer"
# }
