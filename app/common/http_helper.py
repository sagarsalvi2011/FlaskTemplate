"""
Http Helper
"""
import uuid

import jwt
import requests
from flask import json, g
from flask_api import status

from app import app
from app.common.role_enum import RoleEnum


def get(url, permission_url=None):
    """
    Get Http Method
    :param url:
    :param permission_url:
    :return:
    """
    headers = {}
    headers['content-type'] = 'application/json'
    if permission_url:
        headers['token'] = get_temporary_token(permission_url, "GET")
    else:
        headers['token'] = get_temporary_token(url, "GET")
    resp = requests.get(url, headers=headers)
    if resp.status_code != status.HTTP_200_OK:
        raise Exception("HTTP get call failed, url - " + url)
    return json.loads(resp.content)


def post(url, data, permission_url=None):
    """
    Post Http Method
    :param url:
    :param data:
    :param permission_url:
    :return:
    """
    headers = {}
    headers['content-type'] = 'application/json'
    if permission_url:
        headers['token'] = get_temporary_token(permission_url, "POST")
    else:
        headers['token'] = get_temporary_token(url, "POST")
    # headers['token'] = get_temporary_token(url, "POST")

    resp = requests.post(url, headers=headers, data=json.dumps(data))
    if resp.status_code != status.HTTP_200_OK:
        raise Exception("HTTP post call failed, url - " + url + ", error code - " + resp.status_code)
    return json.loads(resp.content)


def get_temporary_token(url, method_string):
    """
    Token
    :param url:
    :param method_string:
    :return:
    """
    permissions = []
    permission_json = {}
    permission_json['url'] = url
    http_methods_json = []
    # http_methods_json.append("GET")
    http_methods_json.append(method_string)
    permission_json['methods'] = http_methods_json
    permissions.append(permission_json)
    from datetime import datetime, timedelta

    if g and hasattr(g, 'current_user'):
        token = jwt.encode({
            'id': g.current_user.id,
            'email': g.current_user.email,
            'role': g.current_user.role_identifier,
            'permissions': permissions,
            'session_identifier': g.current_user.session_identifier,
            'exp': datetime.utcnow() + timedelta(
                seconds=app.config.get('JWT_EXPIRATION_DELTA')),
            'iat': datetime.utcnow()},
            app.config.get('SECRET_KEY'))
    else:
        token = jwt.encode({
            'id': 0,
            'email': "admin@gmail.com",
            'role': RoleEnum.SUPER_ADMIN,
            'permissions': permissions,
            'session_identifier': uuid.uuid3(uuid.NAMESPACE_DNS, 'gmail.com').hex,
            'exp': datetime.utcnow() + timedelta(
                seconds=app.config.get('JWT_EXPIRATION_DELTA')),
            'iat': datetime.utcnow()},
            app.config.get('SECRET_KEY'))
    return token
