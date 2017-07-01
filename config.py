"""
This file holds all of the Flask
application configuration
"""
from datetime import timedelta
from app import app
import os

class Config(object):
    """
    Base Configuration Class
    Contains all Application Constant
    Defaults
    """
    DEBUG = True
    SECRET_KEY = 'Eg=C}k!5]YG`d{*`#dDZd4=*#'
    RESTFUL_JSON = {"cls": app.json_encoder}
    JWT_EXPIRATION_DELTA = 60
    JWT_AUTH_URL_RULE = '/v1/api/auth'

    DEBUG = True
    PORT = 5000
    HOST = "0.0.0.0"

    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'root')
    db_pass = os.getenv('DB_PASS', 'fr3sca')


    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/demo'.format(db_user, db_pass, db_host)
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_TIMEOUT = 10
    SQLALCHEMY_POOL_RECYCLE = 500
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APPLICATION_ROOT = '/ums'


class ProductionConfig(Config):
    """
    Any Production necessary modifications
    to Config object
    Turns off DEBUG
    """
    print 'ProductionConfig'

class TestingConfig(Config):
    """
    Contains settings and modifications
    for development environment
    """
    print 'TestingConfig'

class DevelopmentConfig(Config):
    """
    Contains settings and modifications
    for development environment
    This is the configuration to use with Docker
    """
    print 'DevelopmentConfig'
