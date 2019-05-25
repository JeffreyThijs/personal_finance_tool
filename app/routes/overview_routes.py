from flask import render_template, flash, redirect, url_for, request, send_file
from flask_login import current_user, login_required
from app.forms.forms import TransactionForm, TranactionButton
from app.tools.dateutils import filter_on_MonthYear, _next_month, _previous_month, dt_parse, MONTHS
from app.sqldb.dbutils import add_new_transaction, edit_transaction
from werkzeug.urls import url_parse
from app.sqldb.models import User
from app import app, db
import json

@app.route('/', methods=['GET', 'POST'])
@app.route('/monthly_overview', methods=['GET', 'POST'])
@login_required
def monthly_overview():
    # new_transaction = TranactionButton()
    # if new_transaction.validate_on_submit():
    #     return redirect(url_for('entry'))

    transactions = list(current_user.transactions)
    transactions.sort(key=lambda x: x.date, reverse=False)

    current_date_view = dt_parse(current_user.last_date_viewed)

    current_month_view, current_year_view = str(current_user.last_date_viewed.month), str(current_user.last_date_viewed.year)
    transactions = filter_on_MonthYear(transactions, "date", current_month_view, current_year_view)

    balance = round(sum(t.price for t in transactions if t.incoming) - sum(t.price for t in transactions if not t.incoming), 2)

    edit_transaction_form = TransactionForm()
    if edit_transaction_form.validate_on_submit():
        print("called")
        print("id: {}, price: {}".format(edit_transaction_form.transaction_id.data, edit_transaction_form.price.data))
        edit_transaction(id=edit_transaction_form.transaction_id.data, 
                         price=edit_transaction_form.price.data)
        return redirect(url_for('monthly_overview'))

    #    new_transaction=new_transaction,
    return render_template('monthly_overview.html',
                           title='Home',
                           transactions=transactions,
                           balance=balance,
                           current_date_view=current_date_view,
                           edit_transaction_form=edit_transaction_form)


@app.route('/next_month', methods=['GET', 'POST'])
@login_required
def next_month():
    current_month = current_user.last_date_viewed.month
    new_month = _next_month(str(current_month))
    current_user.last_date_viewed = current_user.last_date_viewed.replace(month=new_month)
    if current_month == 12:
        current_year = current_user.last_date_viewed.year
        current_user.last_date_viewed = current_user.last_date_viewed.replace(year=current_year+1)
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('monthly_overview'))

@app.route('/previous_month', methods=['GET', 'POST'])
@login_required
def previous_month():
    current_month = current_user.last_date_viewed.month
    new_month = _previous_month(str(current_month))
    current_user.last_date_viewed = current_user.last_date_viewed.replace(month=new_month)
    if current_month == 1:
        current_year = current_user.last_date_viewed.year
        current_user.last_date_viewed = current_user.last_date_viewed.replace(year=current_year-1)
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('monthly_overview'))

@app.route('/entry', methods=['GET', 'POST'])
@login_required
def entry():
    form = TransactionForm()
    if form.validate_on_submit():
        add_new_transaction(price=form.price.data,
                            date=form.date.data,
                            comment=form.comment.data,
                            category=form.category.data,
                            user_id=current_user.id,
                            incoming=form.incoming.data)
        return redirect(url_for('monthly_overview'))
    return render_template('entry.html', title='Entry', form=form)