from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, SelectField, HiddenField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.sqldb.models import User, Transaction
class ChangeDateForm(FlaskForm):
    change_date_id = HiddenField()

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
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
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
    category = SelectField("Category",  choices = Transaction.TransactionType.choices(),
                                        coerce = Transaction.TransactionType.coerce)
    incoming = BooleanField('Incoming transaction')

class EditTransactionForm(TransactionForm):
    transaction_id = HiddenField()

class TransactionRemovalForm(FlaskForm):
    remove_transaction_id = HiddenField()