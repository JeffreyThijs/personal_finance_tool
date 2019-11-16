from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, FloatField, SelectField, HiddenField
from wtforms.validators import DataRequired
from app.sqldb.models import Prognosis

class ChangeDateForm(FlaskForm):
    change_date_id = HiddenField()

class PrognosisForm(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    comment = StringField('Comment', validators=[DataRequired()])
    occurance_type = SelectField("Occurance",  choices = Prognosis.PrognosisOccuranceType.choices(),
                                               coerce = Prognosis.PrognosisOccuranceType.coerce)
    incoming = BooleanField('Incoming prognosis')

class EditPrognosisForm(PrognosisForm):
    prognosis_id = HiddenField()

class PrognosisRemovalForm(FlaskForm):
    remove_prognosis_id = HiddenField()