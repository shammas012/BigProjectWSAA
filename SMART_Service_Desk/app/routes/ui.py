from flask import Blueprint, render_template
from app.models import Ticket

bp = Blueprint('ui', __name__)

@bp.route('/home')
def dashboard():
    total = Ticket.query.count()
    return render_template('home.html', total=total)
