from apps import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    customer_name = db.Column(db.String(40), nullable=False)
    email_address = db.Column(db.String(60), index=True, unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    insurances = db.relationship('Insurance', backref='user', lazy='dynamic')
    userprofiles = db.relationship('UserProfile', backref='customerprofile', lazy='dynamic')

    def __init__(self, customer_name, email_address, password):
        self.customer_name = customer_name
        self.email_address = email_address
        self.password = password

    def __str__(self):
        return f"{self.customer_name}"
    
    def __repr__(self):
        return f"Customer({self.customer_name})"

class UserProfile(db.Model):
    __tablename__ = 'userprofile'

    id = db.Column(db.Integer, primary_key = True)
    activation_status = db.Column(db.String(10), nullable=False)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, activation_status, customerprofile):
        self.activation_status = activation_status
        self.customerprofile = customerprofile

    def __str__(self):
        return f"{self.activation_status}"
    
    def __repr__(self):
        return f"UserProfile({self.activation_status})"
    
class InsurancePlan(db.Model):
    __tablename__ = 'insuranceplan'

    id = db.Column(db.Integer, primary_key = True)
    insurance_plan_name = db.Column(db.String(200), unique=True, nullable=False)
    insurances = db.relationship('Insurance', backref='insurance_plan', lazy='dynamic')

    def __init__(self, insurance_plan_name):
        self.insurance_plan_name = insurance_plan_name

    def __str__(self):
        return f"{self.insurance_plan_name}"
    
    def __repr__(self):
        return f"InsurancePlan({self.insurance_plan_name})"
    
class Insurance(db.Model):
    __tablename__ = 'insurance'

    id = db.Column(db.Integer, primary_key = True)
    insured_amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    insurance_plan_id = db.Column(db.Integer, db.ForeignKey('insuranceplan.id'), nullable=False)

    def __init__(self, insured_amount, user, insurance_plan):
        self.insured_amount = insured_amount
        self.user = user
        self.insurance_plan = insurance_plan

    def __str__(self):
        return f"{self.insured_amount}"
    
    def __repr__(self):
        return f"Insurance({self.insured_amount})"

class Blacklist(db.Model):
    __tablename__ = 'blacklist'

    id = db.Column(db.Integer, primary_key = True)
    email_address = db.Column(db.String(60), index=True, unique=True, nullable=False)
    reason = db.Column(db.String(100))

    def __init__(self, email_address, reason):
        self.email_address = email_address
        self.reason = reason

    def __str__(self):
        return f"{self.email_address}"
    
    def __repr__(self):
        return f"Blacklist Email({self.email_address})"
