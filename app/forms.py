from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class TranactionButton(FlaskForm):
    submit = SubmitField('New Transaction')

class TaxForm(FlaskForm):
    gross_wage = FloatField('Price', validators=[DataRequired()])
    submit = SubmitField('Calculate')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class TransactionForm(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    comment = StringField('Comment', validators=[DataRequired()])
    incoming = BooleanField('Incoming transaction')

    submit = SubmitField('Add Transaction')
