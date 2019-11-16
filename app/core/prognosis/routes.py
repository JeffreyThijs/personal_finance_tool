from flask import render_template, redirect, url_for
from flask_login import login_required
from app.sqldb.prognoses import get_user_prognoses, add_new_prognosis
from app.core.prognosis import bp
from app.core.prognosis.form_handler import FormHandler

@bp.route('/yearly_overview', methods=['GET', 'POST'])
@login_required
def yearly_overview():
    # init form handler
    f = FormHandler()
    # get prognoses
    prognoses = get_user_prognoses()
    # handle forms
    if f.handle_forms():
        return redirect(url_for('prognosis.yearly_overview'))  

    return render_template('core/prognosis/yearly_overview.html',
                           prognoses=prognoses,
                           forms=f.forms)