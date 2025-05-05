from flask import Blueprint, render_template, request
from app.models import Ticket, User, db
from app.routes.utils import log_exceptions

bp = Blueprint('ui', __name__)

@bp.route('/home')
def dashboard():
    total = Ticket.query.count()
    return render_template('home.html', total=total)


@bp.route('/tickets')
def view_tickets():
    page = int(request.args.get('page', 1))
    per_page = 50
    offset = (page - 1) * per_page

    tickets = Ticket.query.order_by(Ticket.createdAt.desc()).offset(offset).limit(per_page).all()
    total = Ticket.query.count()

    return render_template('tickets.html', tickets=tickets, total=total, offset=offset, page=page, per_page=per_page)

@bp.route('/tickets/<key>')
def ticket_detail(key):
    ticket = Ticket.query.filter_by(key=key).first_or_404()
    users = User.query.order_by(User.fullname).all()
    return render_template('ticketDetails.html', ticket=ticket, users = users)

@bp.route('/debug-users')
def debug_user_ids():
    users = User.query.all()
    return "<br>".join([f"id: {u.id}, fullname: {u.fullname}, username: {u.username}" for u in users])


@bp.route('/tickets/<key>', methods=['PATCH'])
@log_exceptions
def update_ticket_field(key):
    data = request.get_json()
    field = data.get("field")
    value = data.get("value")

    ticket = Ticket.query.filter_by(key=key).first()
    if not ticket:
        return {"error": "Ticket not found"}, 404

    try:
        setattr(ticket, field, value)
        ticket.updatedAt = db.func.now()
        db.session.commit()
        return {"message": f"{field} updated"}, 200
    except Exception as ex:
        db.session.rollback()
        return {"error": f"Failed to update field: {str(ex)}"}, 500


@bp.route('/users')
def view_users():
    page = int(request.args.get('page', 1))
    per_page = 50
    offset = (page - 1) * per_page

    users = User.query.order_by(User.createdAt.desc()).offset(offset).limit(per_page).all()
    total = User.query.count()

    return render_template('users.html', users=users, total=total, offset=offset, page=page, per_page=per_page)