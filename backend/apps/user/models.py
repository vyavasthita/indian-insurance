from apps import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    customer_name = db.Column(db.String(40))
    email_address = db.Column(db.String(50))
    insurance_plan_name = db.Column(db.String(200))
    insured_amount = db.Column(db.Integer)