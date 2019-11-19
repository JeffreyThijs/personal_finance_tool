from flask import render_template, redirect, url_for
from flask_login import login_required
from app.core.prognosis import bp
from app.core.prognosis.form_handler import FormHandler
from app.core.prognosis.helpers import get_prognosis_data
import datetime

@bp.route('/yearly_overview', methods=['GET', 'POST'])
@login_required
def yearly_overview():
    # init form handler
    f = FormHandler()

    # get year
    year = datetime.datetime.now().year

     # make table title
    table_title = "Prognosis " + str(year)

    # handle forms
    if f.handle_forms():
        return redirect(url_for('prognosis.yearly_overview'))  

    # get prognoses
    data = get_prognosis_data(year)
    
    return render_template('core/prognosis/yearly_overview.html',
                           table_title=table_title,
                           data=data,
                           forms=f.forms)