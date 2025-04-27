# references
# https://docs.python.org/3/library/functools.html#functools.wraps
# https://flask.palletsprojects.com/en/latest/appcontext/#flask.current_app
# https://flask.palletsprojects.com/en/latest/api/#flask.json.jsonify
# https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
# https://blog.miguelgrinberg.com/post/how-to-add-a-production-grade-logger-to-your-flask-application

from flask import jsonify, current_app
from functools import wraps

def log_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            current_app.logger.error(f"Exception in {func.__name__}: {str(ex)}")
            return jsonify({"error": "Internal Server Error"}), 500
    return wrapper