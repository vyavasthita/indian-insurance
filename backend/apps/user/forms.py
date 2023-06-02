from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields import StringField, EmailField, IntegerField, SubmitField


class UserRegistrationForm(FlaskForm):
    customer_name = StringField('Name', validators=[DataRequired()])
    email_address = EmailField('Email Address', validators=[DataRequired()])
    insurance_plan_name = StringField('Insurance Plan', validators=[DataRequired()])
    insured_amount = IntegerField('Insurance Amount', validators=[DataRequired()])

    submit = SubmitField('Sign Up')