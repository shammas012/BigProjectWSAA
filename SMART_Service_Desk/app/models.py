from datetime import datetime
from . import db
import uuid as guid

def generateGuid():
    return str(guid.uuid4())

class UserRole(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.String(100), primary_key = True, default = generateGuid)
    description = db.Column(db.String(100), unique=True)

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description
        }

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(100), primary_key = True, default = generateGuid)
    username = db.Column(db.String(100))
    fullname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    roleid = db.Column(db.String(100), db.ForeignKey('user_roles.id'))

    def serializeJson(self):
        return {
            'id': self.id,
            'username': self.username,
            'fullname': self.fullname,
            'email': self.email,
            'roleid': self.roleid
        }

class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.String(100), primary_key=True, default=generateGuid)
    name = db.Column(db.String(100), unique=True, nullable=False)
    shortName = db.Column(db.String(10), unique=True, nullable=False)
    createdBy = db.Column(db.String(100), db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    tickets = db.relationship('Ticket', backref='project')
    def serializeJson(self):
        return {
            'id': self.id,
            'name': self.name,
            'shortName': self.shortName,
            'createdBy': self.createdBy,
            'timestamp': self.timestamp
        }


class IssueType(db.Model):
    __tablename__ = "issue_types"
    id = db.Column(db.String(100), primary_key = True, default = generateGuid)
    description = db.Column(db.String(100), unique=True)
    def serializeJson(self):
        return {
            'id': self.id,
            'description': self.description
        }

class WorkflowStatus(db.Model):
    __tablename__ = "workflow_statuses"
    id = db.Column(db.String(100), primary_key = True, default = generateGuid)
    description = db.Column(db.String(100), unique=True)
    is_terminal = db.Column(db.Boolean, default=False)
    is_default = db.Column(db.Boolean, default=False)


class WorkflowTransition(db.Model):
    __tablename__ = "workflow_transitions"
    id = db.Column(db.String(100), primary_key = True, default = generateGuid)
    fromStatus = db.Column(db.String(100), db.ForeignKey('workflow_statuses.id'))
    toStatus = db.Column(db.String(100), db.ForeignKey('workflow_statuses.id'))


class Ticket(db.Model):
    __tablename__ = "tickets"
    key = db.Column(db.String(100), primary_key = True)
    summary = db.Column(db.String(100))
    description = db.Column(db.String(500))
    createdBy = db.Column(db.String(100), db.ForeignKey('users.id'))
    assignedTo = db.Column(db.String(100), db.ForeignKey('users.id'))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow)
    issueTypeId = db.Column(db.String(100), db.ForeignKey('issue_types.id'))
    statusId = db.Column(db.String(100), db.ForeignKey('workflow_statuses.id'))
    issueType = db.relationship('IssueType', backref='tickets')
    projectId = db.Column(db.String(100), db.ForeignKey('projects.id'))

class TicketHistory(db.Model):
    __tablename__ = "ticket_history"
    id = db.Column(db.String(100), primary_key = True, default = generateGuid)
    ticketKey = db.Column(db.String(100), db.ForeignKey('tickets.key'))
    fromStatus = db.Column(db.String(100))
    toStatus = db.Column(db.String(100))
    changed_by = db.Column(db.String(100), db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
