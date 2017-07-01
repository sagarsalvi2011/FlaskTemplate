#!/usr/bin/env python

"""
User Service provides all business logic around user entity.
"""

from app.module.models import User
from marshmallow import ValidationError
from sqlalchemy import exc

from app import db
from app.common.database_operation_failed_error import DatabaseOperationFailedError


class UserService(object):
    """
    User service
    """

    def customer_signup(self, data):
        """
        registers new User
        :param data:
        :return: returns updated user object
        """
        session = db.session()
        try:
            inactive_user = User.query.filter_by(email=data['email'],
                                                 is_active=False,
                                                 is_deleted=False).first()
            if inactive_user:
                raise ValidationError("User already exist, Please activate your account.")

            # request data is already validated now lets convert it to a model object
            user = User(**data)

            # Currently we set user in active state
            user.is_active = False
            user.is_deleted = False
            if 'password' not in data:
                raise ValidationError("Password required.")
            self.check_user_is_present(session, user)
            session.add(user)
            session.commit()
            return user
        except ValidationError as exception:
            session.rollback()
            raise DatabaseOperationFailedError(exception.message)
        except exc.SQLAlchemyError as exception:
            session.rollback()
            raise DatabaseOperationFailedError(exception.message)
        except Exception as exception:
            session.rollback()
            raise DatabaseOperationFailedError(exception.message)

    def check_user_is_present(self, session, user):
        '''
        :param user:
        :return:
        '''
        user_not_present = User.query.filter_by(email=user.email, is_deleted=True, is_active=False).first()
        user_already_exist = User.query.filter_by(email=user.email, is_deleted=False, is_active=True).first()
        if user_not_present:
            session.delete(user_not_present)
        elif user_already_exist:
            raise ValidationError("User already exists.")