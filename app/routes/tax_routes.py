from flask import render_template
from flask_login import login_required
from app.forms.forms import TaxForm
from app.tools.taxutils import calc_net_wage
from app import app, db

@app.route('/tax', methods=['GET', 'POST'])
@login_required
def tax():
    form = TaxForm()
    net_wage = calc_net_wage(form.gross_wage.data) if form.validate_on_submit() else -1
    return render_template('tax.html', title='Tax', form=form, net_wage=net_wage)