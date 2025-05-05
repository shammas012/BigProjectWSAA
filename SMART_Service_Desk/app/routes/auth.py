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
        current_app.logger.info(f"Created user {user.username}.")

        return jsonify(user.serializeJson()), 201
    
    except Exception as ex:
        db.session.rollback()  
        current_app.logger.error(f"Failed to create user: {str(ex)}")
        return jsonify({"error": "Failed to create user"}), 500