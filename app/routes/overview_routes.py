from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from app.tools.dateutils import filter_on_MonthYear, _next_month, _previous_month, generic_datetime_parse, MONTHS, date_time_parse
from app.sqldb.models import User, Transaction
from app import app, db
from app.forms.form_handler import FormHandler

@app.route('/', methods=['GET', 'POST'])
@app.route('/monthly_overview', methods=['GET', 'POST'])
@login_required
def monthly_overview():

    f = FormHandler()

    transactions = list(current_user.transactions)
    transactions.sort(key=lambda x: x.date, reverse=False)

    current_date_view = generic_datetime_parse(current_user.last_date_viewed, format='%B %Y')

    current_month_view, current_year_view = str(current_user.last_date_viewed.month), str(current_user.last_date_viewed.year)
    transactions = filter_on_MonthYear(transactions, "date", current_month_view, current_year_view)

    balance = round(sum(t.price for t in transactions if t.incoming) - sum(t.price for t in transactions if not t.incoming), 2)

    # for i in range(len(transactions)):
    #     transactions[i].category = Transaction.TransactionType(transactions[i].type).name

    # handle forms
    if f.handle_forms():
        return redirect(url_for('monthly_overview'))  

    return render_template('monthly_overview.html',
                           transactions=transactions,
                           balance=balance,
                           current_date_view=current_date_view,
                           forms=f.forms)


@app.route('/next_month', methods=['GET', 'POST'])
@login_required
def next_month():
    current_month = current_user.last_date_viewed.month
    new_month = _next_month(str(current_month))
    current_user.last_date_viewed = current_user.last_date_viewed.replace(day=1, month=new_month)
    if current_month == 12:
        current_year = current_user.last_date_viewed.year
        current_user.last_date_viewed = current_user.last_date_viewed.replace(day=1, year=current_year+1)
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('monthly_overview'))

@app.route('/previous_month', methods=['GET', 'POST'])
@login_required
def previous_month():
    current_month = current_user.last_date_viewed.month
    new_month = _previous_month(str(current_month))
    current_user.last_date_viewed = current_user.last_date_viewed.replace(day=1, month=new_month)
    if current_month == 1:
        current_year = current_user.last_date_viewed.year
        current_user.last_date_viewed = current_user.last_date_viewed.replace(day=1, year=current_year-1)
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('monthly_overview'))