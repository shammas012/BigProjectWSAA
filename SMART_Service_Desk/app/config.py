import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql://root:Aturoot@localhost:3306/smart_ticket_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False