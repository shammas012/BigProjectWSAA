#references
# https://realpython.com/flask-by-example-part-1-project-setup/
# https://flask.palletsprojects.com/en/stable/api/#flask.json.jsonify
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# https://realpython.com/flask-blueprint/
# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy
# https://flask.palletsprojects.com/en/latest/logging/
# https://docs.sqlalchemy.org/en/20/orm/session_basics.html
# https://stackoverflow.com/questions/63750482/flask-check-password-always-return-false
# https://realpython.com/token-based-authentication-with-flask/#logout-route-handler


from flask import Blueprint, redirect, request, jsonify, current_app, render_template, make_response, url_for
from app.models import User
from app import db
from app.routes.utils import log_exceptions
from flask_jwt_extended import create_access_token



bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST'])
@log_exceptions  
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")  

        user = User.query.filter_by(username=username).first()

        if not user or not user.password_hash:
            current_app.logger.warning(f"Login failed for unknown user: {username}")
            return jsonify({"error": "Invalid username or password"}), 401

        if not user.check_password(password):
            current_app.logger.warning(f"Login failed for user: {username} (incorrect password)")
            return jsonify({"error": "Invalid username or password"}), 401

        access_token = create_access_token(identity=user.id)
        resp = make_response(jsonify({
            "message": "Login successful",
            "access_token": access_token
            }))
        resp.set_cookie('access_token_cookie', access_token, httponly=True)
        current_app.logger.info(f"Login successful for user: {username}")
        return resp

    except Exception as ex:
        current_app.logger.error(f"Exception in login: {str(ex)}")
        return jsonify({"error": "Internal Server Error"}), 500

@bp.route('/login', methods=['GET'])
@log_exceptions
def login_form():
    return render_template('login.html')

@bp.route('/logout', methods=['POST'])
@log_exceptions
def logout():
    resp = make_response(redirect(url_for('auth.login_form')))
    resp.delete_cookie('access_token_cookie')
    return resp