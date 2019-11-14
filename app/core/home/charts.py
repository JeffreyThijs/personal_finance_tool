from app.tools.dateutils import filter_on_MonthYear, MONTHS, partition_in_MonthYear
from app.sqldb.models import Transaction
import datetime

def get_donut_charts_data(transactions):

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

def get_bar_charts_data(transactions, year=datetime.datetime.now().year):

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

def get_line_charts_data(transactions):

    line_data = {"labels" : [],
                 "monthly_balance" : []}

    transactions_monthly = partition_in_MonthYear(transactions, "date")

    _balance = 0
    for year in transactions_monthly:
        for month in transactions_monthly[year]:
            _balance += (  sum([t.price for t in transactions_monthly[year][month] if t.incoming]) 
                         - sum([t.price for t in transactions_monthly[year][month] if not t.incoming]))
            line_data["labels"].append("{} {}".format(month, year))
            line_data["monthly_balance"].append(round(_balance, 2))
            
    return line_data