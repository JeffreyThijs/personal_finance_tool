from flask import render_template, redirect, url_for
from flask_login import login_required
from app.core.prognosis import bp
from app.core.prognosis.form_handler import FormHandler
from app.core.prognosis.helpers import get_prognosis_data

@bp.route('/yearly_overview', methods=['GET', 'POST'])
@login_required
def yearly_overview():
    # init form handler
    f = FormHandler()
    # get prognoses
    data = get_prognosis_data(2019)
    # handle forms
    if f.handle_forms():
        return redirect(url_for('prognosis.yearly_overview'))  

    return render_template('core/prognosis/yearly_overview.html',
                           data=data,
                           forms=f.forms)