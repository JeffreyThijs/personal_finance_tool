from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app.forms.forms import TransactionForm, TranactionButton, TaxForm
from app.tools.dateutils import filter_on_MonthYear, MONTHS
from werkzeug.urls import url_parse
from app.sqldb.models import User
from app import app, db

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    dates = []
    current_date = None
    current_balance = 0.0
    balance_history = []
    incoming_data, outgoing_data = [], []
    
    transactions = list(current_user.transactions)
    transactions.sort(key=lambda x: x.date, reverse=False)

    for t in transactions:
        if t.incoming:
            current_balance += t.price
        else:
            current_balance -= t.price

        current_date = t.date

        if len(dates) == 0 or current_date != dates[-1:]:
            dates.append(current_date)
            balance_history.append(round(current_balance, 0))

    sdates = [dt.strftime("%d/%m/%Y") for dt in dates]
    labels = sdates

    for month in MONTHS:
        sum_incoming, sum_outgoing = 0, 0
        ts = filter_on_MonthYear(transactions, "date", month, "2019")
        for t in ts:
            if t.incoming:
                sum_incoming += t.price
            else:
                sum_outgoing += t.price
        incoming_data.append(round(sum_incoming, 2))
        outgoing_data.append(round(sum_outgoing, 2))

    overall_data = balance_history
    return render_template('index.html', 
                            title='Plots', 
                            labels=labels, 
                            overall_data=overall_data, 
                            labels_bar=MONTHS,
                            incoming_data=incoming_data,
                            outgoing_data=outgoing_data)