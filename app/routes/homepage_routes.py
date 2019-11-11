from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app.forms.forms import TransactionForm, TaxForm
from app.tools.dateutils import filter_on_MonthYear, MONTHS, partition_in_MonthYear
from werkzeug.urls import url_parse
from app.sqldb.models import User, Transaction
from app import app, db
import datetime

def _get_donut_charts_data(transactions):

    donut_data = {}
    donut_data["labels"] = [c[1] for c in Transaction.TransactionType.choices()]
    donut_data["incoming"] =  [0] * len(donut_data["labels"])
    donut_data["outgoing"] =  [0] * len(donut_data["labels"])

    for t in transactions:
        _index = donut_data["labels"].index(Transaction.TransactionType(t.type).name.title())
        if t.incoming:
            donut_data["incoming"][_index] += t.price
        else:
            donut_data["outgoing"][_index] += t.price

    donut_data["incoming"] = [round(x, 2) for x in donut_data["incoming"]]
    donut_data["outgoing"] = [round(x, 2) for x in  donut_data["outgoing"]]

    return donut_data

def _get_bar_charts_data(transactions, year=datetime.datetime.now().year):

    bar_data = {"labels" : MONTHS,
                "incoming" : [],
                "outgoing" : []}

    for month in bar_data["labels"]:
        sum_incoming, sum_outgoing = 0, 0
        ts = filter_on_MonthYear(transactions, "date", month, str(year))
        for t in ts:
            if t.incoming:
                sum_incoming += t.price
            else:
                sum_outgoing += t.price

        bar_data["incoming"].append(round(sum_incoming, 2))
        bar_data["outgoing"].append(round(sum_outgoing, 2))

    return bar_data

def _get_line_charts_data(transactions):

    line_data = {"labels" : [],
                 "monthly_balance" : []}

    transactions_montly = partition_in_MonthYear(transactions, "date")

    _balance = 0
    for year in transactions_montly:
        for month in transactions_montly[year]:
            _balance += (  sum([t.price for t in transactions_montly[year][month] if t.incoming]) 
                         - sum([t.price for t in transactions_montly[year][month] if not t.incoming]))
            line_data["labels"].append("{} {}".format(month, year))
            line_data["monthly_balance"].append(round(_balance, 2))
            
    return line_data

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    transactions = list(current_user.transactions)
    transactions.sort(key=lambda x: x.date, reverse=False)

    donut_data = _get_donut_charts_data(transactions)
    bar_data = _get_bar_charts_data(transactions)
    line_data = _get_line_charts_data(transactions)

    return render_template('index.html', 
                            line_data=line_data,
                            bar_data=bar_data,
                            donut_data=donut_data)