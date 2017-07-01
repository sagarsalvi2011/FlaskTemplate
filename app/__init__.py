#!/usr/bin/env python

"""
Main Run File for Flask Application
"""

import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, Response
from flask_api import status
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from app.common.permission_error import PermissionError

SETTINGS = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'production': 'config.ProductionConfig',
}


class MyResponse(Response):
    """
    Default Response
    """
    default_mimetype = 'application/json'


# create app object which is global to a runtime environment
app = Flask(__name__)
CONFIG = os.getenv('FLASK_CONFIGURATION', 'development')
print "Loading configuration for the environment : %s" % CONFIG
app.config.from_object(SETTINGS[CONFIG])

# set out response object which will be always in json format
app.response_class = MyResponse

CORS(app)

# Initialise SQLAlchemy with our application object
db = SQLAlchemy(app)

# Initialise REST API's with our application object
api = Api(app)

current_user = None

# Logger configuration
log_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir) + os.path.sep + 'log'
if not os.path.exists(log_path):
    os.makedirs(log_path)
formatter = logging.Formatter(
    "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler = RotatingFileHandler(log_path + os.path.sep + 'app.log', maxBytes=10000000, backupCount=1)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.debug("Logger Initiated")
logger = app.logger


@app.errorhandler(Exception)
def handle_permission_error(error):
    """
    :param error:
    :return:
    """
    from app.common.utils import response
    return response("", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=error)


# Used for App db migrations and upgrades
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
