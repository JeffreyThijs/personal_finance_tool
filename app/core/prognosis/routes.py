from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.core.prognosis import bp
from app.core.prognosis.form_handler import FormHandler
from app.core.prognosis.helpers import get_prognosis_data, transition_yearly_overview
import datetime

@bp.route('/yearly_overview', methods=['GET', 'POST'])
@login_required
def yearly_overview():
    # init form handler
    f = FormHandler()

    # get year
    year = current_user.last_prognosis_viewed.year \
           if current_user.last_prognosis_viewed else datetime.datetime.now().year

     # make table title
    table_title = "Prognosis " + str(year)

    # handle forms
    if f.handle_forms():
        return redirect(url_for('prognosis.yearly_overview'))  

    # get prognosesprevious_year
    data = get_prognosis_data(year)
    
    return render_template('core/prognosis/yearly_overview.html',
                           table_title=table_title,
                           data=data,
                           current_date_view=str(year),
                           forms=f.forms)

@bp.route('/next_year', methods=['GET', 'POST'])
@login_required
def next_year():
    transition_yearly_overview(increment=True)
    return redirect(url_for('prognosis.yearly_overview'))

@bp.route('/previous_year', methods=['GET', 'POST'])
@login_required
def previous_year():
    transition_yearly_overview(increment=False)
    return redirect(url_for('prognosis.yearly_overview'))