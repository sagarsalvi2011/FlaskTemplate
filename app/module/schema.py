#!/usr/bin/env python

"""
Database Model for the entity User
"""
from marshmallow import Schema, fields, validates_schema, ValidationError
from validate_email import validate_email

from app.common import free_email_domains
from app.common.schema_utils import must_not_be_blank, password_format_validation, zipcode_format_validation, phone_number_validation
from app.module.models import User


def email_format_validation(email, user_id=None):
    """
    :param email:
    :param user_id:
    :return: Error message
    """
    if not email:
        return
    if not validate_email(email):
        raise ValidationError('Email is not valid', ['email'])
    if email.split('@')[1] in free_email_domains:
        raise ValidationError('Please signup with corporate email', ['email'])
    query = User.query.filter_by(email=email)
    if user_id:
        query.filter_by(id=user_id)
    if query.first():
        raise ValidationError('User already exists with same email id.', ['email'])


def validate_user_email(email):
    """
    :param email:
    :return: Error message
    """
    if not User.query.filter_by(email=email).first():
        raise ValidationError('Invalid user email', ['email'])


class UserSchema(Schema):
    """
    User schema
    """
    id = fields.Int(required=False)
    email = fields.Email(required=True, validate=must_not_be_blank)
    first_name = fields.Str(required=False, validate=must_not_be_blank)
    last_name = fields.Str(required=False, validate=must_not_be_blank)
    password = fields.Str(required=False, validate=password_format_validation)

    industry_id = fields.Int(required=False)
    manager_id = fields.Int(required=False)
    pre_sales_id = fields.Int(required=False)

    address_line1 = fields.Str(required=False, validate=must_not_be_blank)
    address_line2 = fields.Str(required=False)
    city = fields.Str(required=False, validate=must_not_be_blank)
    zip = fields.Str(required=False, validate=zipcode_format_validation)
    state = fields.Str(required=False, validate=must_not_be_blank)
    company_id = fields.Int(required=False)
    company_name = fields.Str(required=False)
    company_website = fields.Str(required=False)
    country_id = fields.Int(required=False)
    phone = fields.Str(required=False, validate=phone_number_validation)

    time_zone = fields.Str(required=False, validate=must_not_be_blank)
    terms_accepted = fields.Boolean(required=False)

    sales_manager = fields.Nested('self', required=False)
    pre_sales = fields.Nested('self', required=False)
    created_by = fields.Nested('self', required=False)
    updated_by = fields.Nested('self', required=False)

    stats = fields.Dict(required=False)

    @validates_schema
    def validate_user_obj(self, data):
        """
        :param data:
        :return:
        """
        print 'validation'