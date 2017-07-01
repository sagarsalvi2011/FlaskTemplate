#!/usr/bin/env python

"""
Database Model for the entity User
"""

import re

from datetime import datetime
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from app import db



class User(db.Model):
    """
    User Module
    """
    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_encrypted = db.Column(db.String(250))
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(100), nullable=True)
    # This is for the Role: Pre-Sales, Ops Engineer, Sales Manager, Ops Manager
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address_line1 = db.Column(db.String(250))
    address_line2 = db.Column(db.String(250))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip = db.Column(db.String(30))
    # This flag should be used for roles: pre-sales, sales manager.
    # Here the assumption is there will only one across system
    is_default = db.Column(db.Boolean)
    terms_accepted = db.Column(db.Boolean)
    time_zone = db.Column(db.String(100), server_default="US/Pacific", nullable=False)
    # pre-sales assigned to a customer
    pre_sales_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    updated_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    updated_date = db.Column(db.DateTime, nullable=False)
    is_deleted = db.Column(db.Boolean, server_default='0', nullable=False)
    is_active = db.Column(db.Boolean, server_default='0', nullable=False)

    # reference objects
    sales_manager = None
    country = None
    industry = None
    pre_sales = None
    created_by = None
    updated_by = None

    session_identifier = None

    stats = {}

    @orm.reconstructor
    def init_on_load(self):
        """
        :return: stats
        """
        if self.manager_id:
            self.sales_manager = User.query.get_or_404(self.manager_id)
        if self.pre_sales_id:
            self.pre_sales = User.query.get_or_404(self.pre_sales_id)
            self.sales_manager = User.query.get_or_404(self.pre_sales.manager_id)
        if self.created_by_id:
            self.created_by = User.query.get_or_404(self.created_by_id)
        if self.updated_by_id:
            self.updated_by = User.query.get_or_404(self.updated_by_id)

    def __init__(self, email=None, password=None, first_name=None, last_name=None,
                 pre_sales_id=None, address_line1=None, address_line2=None, city=None, state=None, zip=None,
                 manager_id=None, terms_accepted=None, is_deleted=False, is_active=False,
                 is_default=False, phone=None, session_identifier=None):
        self.email = email
        if password:
            self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name

        self.pre_sales_id = pre_sales_id

        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.city = city
        self.state = state
        self.zip = zip

        self.manager_id = manager_id

        self.terms_accepted = terms_accepted

        self.is_deleted = is_deleted
        self.is_active = is_active

        self.updated_date = datetime.utcnow()
        self.created_date = datetime.utcnow()
        self.phone = phone

        # default user is always created by seed data or by super-admin
        self.is_default = is_default
        self.session_identifier = session_identifier

    def set_password(self, password):
        """
        Performs update operation to set password
        :param password: Password to be set
        """
        self.password_encrypted = generate_password_hash(password)

    def check_password(self, password):
        """
        Performs check operation for password
        :param password: password to be checked.
        :return: Checked password hash
        """
        return check_password_hash(self.password_encrypted, password)

    def validate_password(self, password):
        """
        Performs password validation
        :param password: password to be validated.
        :return: Success message if password is validated otherwise error message.
        """

        if password:
            pass
        else:
            return {"error": "Did not receive a password"}

        if len(password) >= 8 and len(password) <= 16:
            pass
        else:
            return {"error": "Password does not meet length requirements"}

        if re.search(r'\d', password):
            pass
        else:
            return {"error": "Password must contain a number"}

        if re.search(r'[A-Z]', password):
            pass
        else:
            return {"error": "Password must contain a capital letter"}

        return {"success": 1}

    def as_dict(self):
        """
        :return: Model to dict
        """
        json_object = {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
        del json_object['password_encrypted']
        return json_object
