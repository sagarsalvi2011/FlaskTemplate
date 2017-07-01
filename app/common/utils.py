"""
This is a utility class used as factory to perform repetitive operations across project to avoid code duplication.

"""
import random
import string
import uuid
from functools import wraps

import jwt
import requests
from datetime import datetime, timedelta
from flask import app
from flask import json, g
from flask import make_response, request
from flask_api import status

from app import logger
from app.module.models import User


class HttpMethods(object):
    """
    Http Method
    """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


def response(msg="", data="", errors=None, status_code=200, exception=None):
    """
    :param msg:
    :param data:
    :param errors:
    :param status_code:
    :param exception:
    :return:
    """
    if errors:
        response_content = {'errors': errors, 'data': data}
    elif exception:
        if hasattr(exception, 'code') and exception.code and exception.code == 404:
            response_content = {'errors': "Couldn't find requested resources to perform action.", 'data': data}
        if hasattr(exception, 'code') and exception.status_code and exception.status_code == 404:
            response_content = {'errors': "Couldn't find requested resources to perform action.", 'data': data}
        else:
            response_content = {'errors': exception.message, 'data': data}
        logger.error(exception)
    else:
        response_content = {'message': msg, 'data': data}
        logger.debug("Response sent: " + json.dumps(response_content))
    http_response = make_response(json.dumps(response_content), status_code)
    http_response.mimetype = 'application/json'
    return http_response


def generate_random_password():
    """
    :return: Random password
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz!@#$%&*_"
    upper_alphabet = alphabet.upper()
    pw_len = 8
    pw_list = []

    for index in range(pw_len // 3):
        logger.info(str(index))
        pw_list.append(alphabet[random.randrange(len(alphabet))])
        pw_list.append(upper_alphabet[random.randrange(len(upper_alphabet))])
        pw_list.append(str(random.randrange(10)))
    for index in range(pw_len - len(pw_list)):
        logger.info(str(index))
        pw_list.append(alphabet[random.randrange(len(alphabet))])

    random.shuffle(pw_list)
    pw_string = "".join(pw_list)
    return pw_string


# def is_auth_required(func):
#     """
#     :param func:
#     :return: check permission
#     """
#
#     @wraps(func)
#     def func_wrapper(*args, **kwds):
#         """
#         :param args:
#         :param kwds:
#         :return:
#         """
#         url = request.path
#         method = request.method
#
#         token = request.headers.get('token')
#         request_json = {'token': token, 'url': url, 'method': method}
#         headers = {}
#         headers['content-type'] = 'application/json'
#         auth_server_url = app.config.get('AUTH_MANAGEMENT_SERVICE_ACCESS_URL') + AUTH_VALIDATE_URL
#         resp = requests.post(auth_server_url, headers=headers, data=json.dumps(request_json))
#         if resp.status_code != status.HTTP_200_OK:
#             return make_response(resp.content, resp.status_code)
#         response_json = json.loads(resp.content)
#         g.current_user = User(response_json['email'], '', None, None, None, None,
#                               role_identifier=response_json['role_identifier'],
#                               session_identifier=response_json['identifier'])
#         g.current_user.id = response_json.get('id')
#         return func(*args, **kwds)
#
#     return func_wrapper


def get_temporary_token(user, url, method_string):
    """
    :param user:
    :param url:
    :param method_string:
    :return: Temporary
    """
    permissions = []
    permission_json = {}
    permission_json['url'] = url
    http_methods_json = []
    http_methods_json.append(method_string)
    permission_json['methods'] = http_methods_json
    permissions.append(permission_json)
    token = jwt.encode({
        'id': user.id,
        'email': user.email,
        'role': user.role_identifier,
        'session_identifier': uuid.uuid3(uuid.NAMESPACE_DNS, 'teradata.com').hex,
        'permissions': permissions,
        'exp': datetime.utcnow() + timedelta(
            minutes=app.config.get('JWT_EXPIRATION_DELTA', 60)),
        'iat': datetime.utcnow()},
        app.config.get('SECRET_KEY'))
    return token


def get_random_password():
    """
    :return: random password
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase + string.digits) for _ in range(16))
