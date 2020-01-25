from flask import render_template, redirect, url_for
from flask_login import login_required
from app.sqldb.api.v1.transactions import get_user_transactions
from app.core.overview.form_handler import FormHandler
from app.core.overview import bp
from app.tools.financeutils import calc_balance
from app.core.overview.helpers import get_current_date_view, get_months_transactions, transition_monthly_overview

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/monthly_overview', methods=['GET', 'POST'])
@login_required
def monthly_overview():
    # init form handler
    f = FormHandler()
    # get current date view
    current_date_view, current_date = get_current_date_view(return_original=True)
    # get transactions of current month view
    transactions = get_months_transactions(current_date)
    # get balance of current transactions
    balance = calc_balance(transactions)

    # handle forms
    if f.handle_forms():
        return redirect(url_for('overview.monthly_overview'))  

    return render_template('core/overview/monthly_overview.html',
                           transactions=transactions,
                           balance=balance,
                           current_date_view=current_date_view,
                           forms=f.forms)

@bp.route('/next_month', methods=['GET', 'POST'])
@login_required
def next_month():
    transition_monthly_overview(increment=True)
    return redirect(url_for('overview.monthly_overview'))

@bp.route('/previous_month', methods=['GET', 'POST'])
@login_required
def previous_month():
    transition_monthly_overview(increment=False)
    return redirect(url_for('overview.monthly_overview'))