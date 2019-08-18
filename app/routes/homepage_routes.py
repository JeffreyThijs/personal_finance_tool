from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app.forms.forms import TransactionForm, TaxForm
from app.tools.dateutils import filter_on_MonthYear, MONTHS, partition_in_MonthYear
from werkzeug.urls import url_parse
from app.sqldb.models import User, Transaction
from app import app, db

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    transactions = list(current_user.transactions)
    transactions.sort(key=lambda x: x.date, reverse=False)
    transactions_montly = partition_in_MonthYear(transactions, "date")

    labels_donut = [c[1] for c in Transaction.TransactionType.choices()]
    incoming_data_donut, outgoing_data_donut = [0] * len(labels_donut), [0] * len(labels_donut)
    for t in transactions:
        _index = labels_donut.index(Transaction.TransactionType(t.type).name.title())
        if t.incoming:
            incoming_data_donut[_index] += t.price
        else:
            outgoing_data_donut[_index] += t.price

    incoming_data_donut = [round(x, 2) for x in incoming_data_donut]
    outgoing_data_donut = [round(x, 2) for x in outgoing_data_donut]

    balance_montly = []
    labels = []
    _balance = 0
    for year in transactions_montly:
        for month in transactions_montly[year]:
            _balance += (sum([t.price for t in transactions_montly[year][month] if t.incoming]) 
                         - sum([t.price for t in transactions_montly[year][month] if not t.incoming]))
            balance_montly.append(round(_balance, 2))
            labels.append("{} {}".format(month, year))

    incoming_data, outgoing_data = [], []
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

    return render_template('index.html', 
                            title='Plots', 
                            labels=labels, 
                            overall_data=balance_montly, 
                            labels_bar=MONTHS,
                            incoming_data=incoming_data,
                            outgoing_data=outgoing_data,
                            labels_donut=labels_donut,
                            incoming_data_donut=incoming_data_donut,
                            outgoing_data_donut=outgoing_data_donut)