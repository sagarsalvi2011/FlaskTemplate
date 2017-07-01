#!/usr/bin/env python

"""
View for the entity User
"""

from app.module.schema import UserSchema
from app.module.service import UserService
from flask import request
from flask_api import status

from app import app
from app.common.database_operation_failed_error import DatabaseOperationFailedError
from app.common.utils import response

USER_SCHEMA = UserSchema()
USER_SERVICE = UserService()


@app.route('/api/v1/users', methods=['POST'])
def customer_signup():
    """
    registers new User of Role: Customer, Sales_Manager, Pre_Sales, OPS_Manager, OPS_Engineer
    :return: returns updated user object
    """
    try:
        # validate the request JSON against User specific validations
        data, errors = USER_SCHEMA.load(request.get_json(force=True))
        if errors:
            # which means JSON received is not valid, report all failed validations to user
            return response(errors=errors, status_code=status.HTTP_412_PRECONDITION_FAILED)

        # add user entry in the database
        USER_SERVICE.customer_signup(data)

        # convert user model object to JSON
        return response(msg="Your account has been successfully registered", status_code=status.HTTP_200_OK)
    except DatabaseOperationFailedError as exception:
        # which means something is wrong with your database/model/request data
        return response(exception.message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        exception=exception)

