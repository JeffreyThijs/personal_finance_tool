from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app.forms.forms import TaxForm
from app.tools.taxutils import calc_net_wage
from werkzeug.urls import url_parse
from app.sqldb.models import User
from app import app, db

@app.route('/tax', methods=['GET', 'POST'])
@login_required
def tax():
    form = TaxForm()
    net_wage = -1
    if form.validate_on_submit():
        net_wage = calc_net_wage(form.gross_wage.data)
    return render_template('tax.html', title='Tax', form=form, net_wage=net_wage)

