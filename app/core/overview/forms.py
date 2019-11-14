from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, FloatField, SelectField, HiddenField
from wtforms.validators import DataRequired
from app.sqldb.models import Transaction

class ChangeDateForm(FlaskForm):
    change_date_id = HiddenField()

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