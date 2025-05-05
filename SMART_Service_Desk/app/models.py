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
    role = db.relationship('UserRole', foreign_keys=[roleid])
    createdBy = db.Column(db.String(100), db.ForeignKey('users.id'))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow)
    Creator = db.relationship('User', foreign_keys=[createdBy], remote_side=[id], backref='users_created_by')

    def serializeJson(self):
        return {
            'id': self.id,
            'username': self.username,
            'fullname': self.fullname,
            'email': self.email,
            'roleid': self.roleid,
            'createdBy': self.createdBy,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
            'updatedAt': self.updatedAt.isoformat() if self.updatedAt else None,
        }

class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.String(100), primary_key=True, default=generateGuid)
    name = db.Column(db.String(100), unique=True, nullable=False)
    shortName = db.Column(db.String(10), unique=True, nullable=False)
    createdBy = db.Column(db.String(100), db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    tickets = db.relationship('Ticket', backref='project')
    lastTicketNumber = db.Column(db.Integer, default=0)  # counter added for the ticket key

    def serializeJson(self):
        return {
            'id': self.id,
            'name': self.name,
            'shortName': self.shortName,
            'createdBy': self.createdBy,
            'lastTicketNumber': self.lastTicketNumber,
            'timestamp': self.timestamp
        }

#Issue Types and workflows inspired from Jira Service Management but in align with ITIL

class IssueType(db.Model):
    __tablename__ = "issue_types"
    id = db.Column(db.String(100), primary_key = True, default = generateGuid)
    description = db.Column(db.String(100), unique=True)
    def serializeJson(self):
        return {
            'id': self.id,
            'description': self.description
        }

#In Phase two the status might need to be tagged against each project, rather than using same statuses/worflows for all projects
class WorkflowStatus(db.Model):
    __tablename__ = "workflow_statuses"
    id = db.Column(db.String(100), primary_key = True, default = generateGuid)
    description = db.Column(db.String(100), unique=True)
    is_terminal = db.Column(db.Boolean, default=False)
    is_default = db.Column(db.Boolean, default=False)
    def serializeJson(self):
        return {
            'id': self.id,
            'description': self.description,
            'is_default': self.is_default,
            'is_terminal': self.is_terminal
        }



class WorkflowTransition(db.Model):
    __tablename__ = "workflow_transitions"
    id = db.Column(db.String(100), primary_key = True, default = generateGuid)
    fromStatus = db.Column(db.String(100), db.ForeignKey('workflow_statuses.id'))
    toStatus = db.Column(db.String(100), db.ForeignKey('workflow_statuses.id'))
    def serializeJson(self):
        return {
            'id': self.id,
            'fromStatus': self.fromStatus,
            'toStatus': self.toStatus
        }


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
    Reporter = db.relationship('User', foreign_keys=[createdBy], backref='created_tickets')
    Assignee = db.relationship('User', foreign_keys=[assignedTo], backref='assigned_tickets')
    status = db.relationship('WorkflowStatus', foreign_keys=[statusId])


    def serializeJson(self):
        return {
            'key': self.key,
            'summary': self.summary,
            'description': self.description,
            'createdBy': self.createdBy,
            'assignedTo': self.assignedTo,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
            'updatedAt': self.updatedAt.isoformat() if self.updatedAt else None,
            'issueTypeId': self.issueTypeId,
            'statusId': self.statusId,
            'projectId': self.projectId
        }

class TicketHistory(db.Model):
    __tablename__ = "ticket_history"
    id = db.Column(db.String(100), primary_key = True, default = generateGuid)
    ticketKey = db.Column(db.String(100), db.ForeignKey('tickets.key'))
    fromStatus = db.Column(db.String(100))
    toStatus = db.Column(db.String(100))
    changedBy = db.Column(db.String(100), db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def serializeJson(self):
            return {
                'id': self.id,
                'ticketKey': self.ticketKey,
                'fromStatus': self.fromStatus,
                'toStatus': self.toStatus,
                'changedBy': self.changedBy,
                'timestamp': self.timestamp.isoformat() if self.timestamp else None
            }