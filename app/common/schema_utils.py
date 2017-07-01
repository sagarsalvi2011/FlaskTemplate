#!/usr/bin/env python

"""
Schema Utils to reduce code duplication
"""

import re

from marshmallow import ValidationError


def validate_filters(obj, filters):
    """
    Validate filters
    :param obj:
    :param filters:
    :return:
    """
    errors = []
    for key in filters:
        if not key in obj.__table__.columns:
            errors.append({key: ['Invalid Filter']})
    return errors


def password_format_validation(password):
    """
    Password format validation
    :param password:
    :return: error message
    """
    password_validation = r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,40})'
    if not re.match(password_validation, password):
        raise ValidationError('Password length should be between 8 to 40 and must contains one digit,\
 one lowercase and one uppercase character.', ['passsword'])


def phone_number_validation(phone_number):
    """
    :param phone_number:
    :return:
    """
    # Cleanup -, space, (, )
    number = re.sub(r'[ \-\(\)]', '', phone_number)
    if not re.match(r'^[0-9]+$', number):
        raise ValidationError('Invalid phone number.', ['phone_number'])


def zipcode_format_validation(zip_code):
    """
    Zipcode Validation
    :param zip_code:
    :return: error message
    """
    zipcode_re = r'^[0-9]+$'
    if not re.match(zipcode_re, zip_code):
        raise ValidationError('Invalid zip code.i.e 12345, 12345-6789', ['zip_code'])


def must_not_be_blank(data, field=None):
    """
    Must not be blank
    :param data:
    :param field:
    :return: error message
    """
    if not data or len(data.strip()) == 0:
        raise ValidationError("can't be blank", field)


def must_be_positive_int(data, field=None):
    """
    Must be positive
    :param data:
    :param field:
    :return: error message
    """
    if data < 1:
        raise ValidationError("Must be a positive integer", field)

def must_be_true(terms):
    """
    :param terms:
    :return: error message
    """
    if not terms:
        raise ValidationError('You must agree with the terms and conditions', ['terms'])
