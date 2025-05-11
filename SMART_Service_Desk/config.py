import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql://root:Aturoot@localhost:3306/smart_ticket_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'fallback-jwt-dev-key')  # Needed by Flask-JWT-Extended
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_COOKIE_SECURE = False  
    JWT_COOKIE_CSRF_PROTECT = False  
