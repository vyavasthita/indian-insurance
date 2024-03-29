"""Models represting database tables

SENECA GLOBAL CONFIDENTIAL & PROPRIETARY

@file models.py
@author Dilip Kumar Sharma
@copyright Seneca Global
@date 2nd Jun 2023

About; -
--------
    DB model for database tables.

Working; -
----------
    This modules creates data modelling for DB tables used in this application.

Uses; -
-------
    This module is used by dao and routes module to access attributes of tables.

Reference; -
------------
    TBD
"""

from apps import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    customer_name = db.Column(db.String(50), nullable=False)
    email_address = db.Column(db.String(50), index=True, unique=True, nullable=False)
    password = db.Column(db.String(200), unique=True, nullable=False)
    insurances = db.relationship('Insurance', backref='user', lazy='dynamic') # One to Many
    userprofiles = db.relationship('UserProfile', backref='customerprofile', uselist=False) # One to One

    def __init__(self, customer_name: str, email_address: str, password: str) -> None:
        self.customer_name = customer_name
        self.email_address = email_address
        self.password = password

    def __str__(self) -> None:
        return f"{self.customer_name}"
    
    def __repr__(self) -> None:
        return f"Customer({self.customer_name})"

class UserProfile(db.Model):
    __tablename__ = 'userprofile'

    id = db.Column(db.Integer, primary_key = True)
    activated = db.Column(db.Boolean, nullable=False, default=False)
    customerprofile_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, customerprofile: User, activated: bool = False) -> None:
        self.customerprofile = customerprofile
        self.activated = activated        

    def __str__(self) -> None:
        return f"UserProfile({self.activated})"
    
    def __repr__(self) ->None:
        return f"UserProfile({self.activated})"
    
class InsurancePlan(db.Model):
    __tablename__ = 'insuranceplan'

    id = db.Column(db.Integer, primary_key = True)
    insurance_plan_name = db.Column(db.String(200), nullable=False)
    insurances = db.relationship('Insurance', backref='insurance_plan', lazy='dynamic')

    def __init__(self, insurance_plan_name: str) -> None:
        self.insurance_plan_name = insurance_plan_name

    def __str__(self) -> None:
        return f"{self.insurance_plan_name}"
    
    def __repr__(self) -> None:
        return f"InsurancePlan({self.insurance_plan_name})"
    
class Insurance(db.Model):
    __tablename__ = 'insurance'

    id = db.Column(db.Integer, primary_key = True)
    insured_amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    insurance_plan_id = db.Column(db.Integer, db.ForeignKey('insuranceplan.id'), nullable=False)

    def __init__(self, insured_amount: int, user: User, insurance_plan: InsurancePlan) -> None:
        self.insured_amount = insured_amount
        self.user = user
        self.insurance_plan = insurance_plan

    def __str__(self) -> None:
        return f"{self.insured_amount}"
    
    def __repr__(self) -> None:
        return f"Insurance({self.insured_amount})"

class Blacklist(db.Model):
    __tablename__ = 'blacklist'

    id = db.Column(db.Integer, primary_key = True)
    email_address = db.Column(db.String(60), index=True, unique=True, nullable=False)
    reason = db.Column(db.String(100))

    def __init__(self, email_address: str, reason: str = None) -> None:
        self.email_address = email_address
        self.reason = reason

    def __str__(self) -> None:
        return f"{self.email_address}"
    
    def __repr__(self) -> None:
        return f"Blacklist Email({self.email_address})"
