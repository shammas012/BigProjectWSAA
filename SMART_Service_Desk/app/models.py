from . import db
import uuid as guid

def generateGuid():
    return str(guid.uuid4())

class UserRole(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.String(100), primary_key = True, default = generateGuid())
    description = db.Column(db.String(100), unique=True)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(100), primary_key = True, default = generateGuid())
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    roleid = db.Column(db.String(100), db.ForeignKey('user_roles.id'))


