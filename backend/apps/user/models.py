from apps import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    customer_name = db.Column(db.String(40))
    email_address = db.Column(db.String(50))
    insurance_plan_name = db.Column(db.String(200))
    insured_amount = db.Column(db.Integer)

    def __init__(self, customer_name, email_address, insurance_plan_name, insured_amount):
        self.customer_name = customer_name
        self.email_address = email_address
        self.insurance_plan_name = insurance_plan_name
        self.insured_amount = insured_amount

    def __str__(self):
        return f"{self.email_address}"