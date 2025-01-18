class Config:
    SECRET_KEY = 'c4904daedb5241ad8f77557727c9217f'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///umebom.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    FLASK_ENV = 'development'