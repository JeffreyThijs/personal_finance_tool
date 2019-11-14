from flask import render_template
from flask_login import login_required
from app.core.tax.forms import TaxForm
from app.tools.taxutils import calc_net_wage
from app import db
from app.core.tax import bp

@bp.route('/tax', methods=['GET', 'POST'])
@login_required
def tax():
    form = TaxForm()
    net_wage = calc_net_wage(form.gross_wage.data) if form.validate_on_submit() else -1
    return render_template('core/tax/tax.html', title='Tax', form=form, net_wage=net_wage)