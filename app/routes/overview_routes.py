from flask import render_template, flash, redirect, url_for, request, send_file
from flask_login import current_user, login_required
from app.forms.forms import TransactionForm, TransactionRemovalForm, ChangeDateForm, EditTransactionForm
from app.tools.dateutils import filter_on_MonthYear, _next_month, _previous_month, generic_datetime_parse, MONTHS, date_time_parse
from app.sqldb.dbutils import add_new_transaction, edit_transaction, remove_transaction
from werkzeug.urls import url_parse
from app.sqldb.models import User, Transaction
from app import app, db
import json

@app.route('/', methods=['GET', 'POST'])
@app.route('/monthly_overview', methods=['GET', 'POST'])
@login_required
def monthly_overview():
    
    transactions = list(current_user.transactions)
    transactions.sort(key=lambda x: x.date, reverse=False)

    current_date_view = generic_datetime_parse(current_user.last_date_viewed, format='%B %Y')

    current_month_view, current_year_view = str(current_user.last_date_viewed.month), str(current_user.last_date_viewed.year)
    transactions = filter_on_MonthYear(transactions, "date", current_month_view, current_year_view)

    balance = round(sum(t.price for t in transactions if t.incoming) - sum(t.price for t in transactions if not t.incoming), 2)

    for i in range(len(transactions)):
        transactions[i].category = Transaction.TransactionType(transactions[i].type).name

    
    edit_transaction_form = EditTransactionForm()
    remove_transaction_form = TransactionRemovalForm()
    change_date_form = ChangeDateForm()
    add_new_transaction_form = TransactionForm()

    # editing current transactions
    if edit_transaction_form.transaction_id.data and edit_transaction_form.validate_on_submit():
        date = date_time_parse(edit_transaction_form.date.data, output_type="datetime", reverse_date=True)
        category = Transaction.TransactionType.coerce(edit_transaction_form.category.data)
        edit_transaction(id=edit_transaction_form.transaction_id.data, 
                         price=edit_transaction_form.price.data,
                         comment=edit_transaction_form.comment.data,
                         category=category,
                         incoming=edit_transaction_form.incoming.data,
                         date=date)
        return redirect(url_for('monthly_overview'))  

    # removing current transaction
    elif remove_transaction_form.remove_transaction_id.data and remove_transaction_form.validate_on_submit():
        remove_transaction(id=remove_transaction_form.remove_transaction_id.data)
        return redirect(url_for('monthly_overview'))  

    # change date
    elif change_date_form.change_date_id.data and change_date_form.validate_on_submit():
        month, year = change_date_form.change_date_id.data.split("-", 1)
        current_user.last_date_viewed = current_user.last_date_viewed.replace(day=1, month=int(month), year=int(year))
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('monthly_overview'))  

    # new transaction
    elif add_new_transaction_form.validate_on_submit():
        add_new_transaction(price=add_new_transaction_form.price.data,
                            date=add_new_transaction_form.date.data,
                            comment=add_new_transaction_form.comment.data,
                            category=add_new_transaction_form.category.data,
                            user_id=current_user.id,
                            incoming=add_new_transaction_form.incoming.data)
        return redirect(url_for('monthly_overview'))


    return render_template('monthly_overview.html',
                           title='Home',
                           transactions=transactions,
                           balance=balance,
                           current_date_view=current_date_view,
                           add_new_transaction_form=add_new_transaction_form,
                           edit_transaction_form=edit_transaction_form,
                           remove_transaction_form=remove_transaction_form,
                           change_date_form=change_date_form)


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