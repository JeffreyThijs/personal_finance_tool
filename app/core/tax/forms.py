from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField
from wtforms.validators import DataRequired

class TaxForm(FlaskForm):
    gross_wage = FloatField('Price', validators=[DataRequired()])
    submit = SubmitField('Calculate')