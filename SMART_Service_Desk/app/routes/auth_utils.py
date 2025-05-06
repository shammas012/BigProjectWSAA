from flask import redirect, url_for
from flask_jwt_extended import verify_jwt_in_request
from functools import wraps

def jwt_required_ui(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception:
            return redirect(url_for('auth.login_form'))  # change if your login route is different
        return view_func(*args, **kwargs)
    return wrapped_view
