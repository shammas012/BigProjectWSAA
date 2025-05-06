from datetime import datetime
from flask import Blueprint, current_app, jsonify, render_template, request
from app.models import Ticket, User, UserRole, db
from app.routes.utils import log_exceptions
from app.routes.auth_utils import jwt_required_ui


bp = Blueprint('ui', __name__)

@bp.route('/home')
@log_exceptions
@jwt_required_ui
def dashboard():
    total = Ticket.query.count()
    return render_template('home.html', total=total)


@bp.route('/tickets')
@log_exceptions
@jwt_required_ui
def view_tickets():
    page = int(request.args.get('page', 1))
    per_page = 50
    offset = (page - 1) * per_page

    tickets = Ticket.query.order_by(Ticket.createdAt.desc()).offset(offset).limit(per_page).all()
    total = Ticket.query.count()

    return render_template('tickets.html', tickets=tickets, total=total, offset=offset, page=page, per_page=per_page)

@bp.route('/tickets/<key>')
@log_exceptions
@jwt_required_ui
def ticket_detail(key):
    ticket = Ticket.query.filter_by(key=key).first_or_404()
    users = User.query.order_by(User.fullname).all()
    return render_template('ticketDetails.html', ticket=ticket, users = users)

@bp.route('/users/<user_id>', methods=['GET'])
@log_exceptions
@jwt_required_ui
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    userRoles = UserRole.query.order_by(UserRole.description).all()
    users = User.query.order_by(User.fullname).all()

    return render_template('userDetails.html', user=user, userRoles=userRoles, users=users)


@bp.route('/debug-users')
@jwt_required_ui
def debug_user_ids():
    users = User.query.all()
    return "<br>".join([f"id: {u.id}, fullname: {u.fullname}, username: {u.username}" for u in users])


@bp.route('/tickets/<key>', methods=['PATCH'])
@jwt_required_ui
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
        ticket.updatedAt = db.func.now() # update the timestamp automatically
        db.session.commit()
        return {"message": f"{field} updated"}, 200
    except Exception as ex:
        db.session.rollback()
        current_app.logger.error(f"Failed to update user: {str(ex)}")
        return {"error": f"Failed to update ticket: {str(ex)}"}, 500


@bp.route('/users')
@log_exceptions
@jwt_required_ui
def view_users():
    page = int(request.args.get('page', 1))
    per_page = 50
    offset = (page - 1) * per_page

    users = User.query.order_by(User.createdAt.desc()).offset(offset).limit(per_page).all()
    total = User.query.count()

    return render_template('users.html', users=users, total=total, offset=offset, page=page, per_page=per_page)


@bp.route('/users/<user_id>', methods=['PATCH'])
@log_exceptions
@jwt_required_ui
def update_user_field(user_id):
    data = request.get_json()
    field = data.get("field")
    value = data.get("value")

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        setattr(user, field, value)
        user.updatedAt = datetime.utcnow()  # update the timestamp automatically
        db.session.commit()
        current_app.logger.info(f"Updated user {user.username}: {field} = {value}")
        return jsonify({"message": f"{field} updated successfully"}), 200
    except Exception as ex:
        db.session.rollback()
        current_app.logger.error(f"Failed to update user: {str(ex)}")
        return jsonify({"error": "Failed to update user"}), 500
    
@bp.route('/users/new', methods=['GET', 'POST'], endpoint='register_user')
@log_exceptions
@jwt_required_ui
def register_user():
    from app.models import User, UserRole, db
    from flask import request, redirect, url_for, flash

    if request.method == 'POST':
        try:
            data = request.form
            password = data.get('password')
            confirm_password = data.get('confirm_password')

            if password != confirm_password:
                flash("Passwords do not match", "danger")
                return redirect(request.url)
            
            new_user = User(
                username=data.get('username'),
                fullname=data.get('fullname'),
                email=data.get('email'),
                roleid=data.get('roleid'),
                createdBy=data.get('createdBy')  # if time allows implement Oauth2/JWT to get the details of logged in user.
            )
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()
            flash(f"User {new_user.username} created successfully.", "success")
            return redirect(url_for('ui.view_users'))
        except Exception as ex:
            db.session.rollback()
            flash(f"Failed to create user: {str(ex)}", "danger")

    return render_template(
            'userDetails.html',
            user=User(), 
            is_new_user=True,  
            userRoles=UserRole.query.all(),
            users=User.query.all()
    )


