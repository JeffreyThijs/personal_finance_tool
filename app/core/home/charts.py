from app.tools.dateutils import filter_on_MonthYear, MONTHS, partition_in_MonthYear
from app.sqldb.models import Transaction
from app import cache
import datetime
from app.core.prognosis.helpers import get_prognosis_data

@cache.memoize(timeout=300)
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

@cache.memoize(timeout=300)
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

    # get prognoses
    prognosis_data = get_prognosis_data(datetime.datetime.now().year)
    bar_data["expected_incoming"] = [prognosis_data[x].incoming for x in prognosis_data.keys() if x != "Totals"]
    bar_data["expected_outgoing"] = [prognosis_data[x].outgoing for x in prognosis_data.keys() if x != "Totals"]

    return bar_data

@cache.memoize(timeout=300)
def get_line_charts_data(transactions):

    line_data = {"labels" : [],
                 "monthly_balance" : []}

    line_data["current_balance"] = (sum([t.price for t in transactions if (t.incoming and (t.date < datetime.datetime.now()))]) -
                                    sum([t.price for t in transactions if (not t.incoming and (t.date < datetime.datetime.now()))]))
    line_data["current_balance"] = round(line_data["current_balance"], 2)
    transactions_monthly = partition_in_MonthYear(transactions, "date")

    _balance = 0
    for year in transactions_monthly:
        for month in transactions_monthly[year]:
            _balance += (  sum([t.price for t in transactions_monthly[year][month] if t.incoming]) 
                         - sum([t.price for t in transactions_monthly[year][month] if not t.incoming]))
            line_data["labels"].append("{} {}".format(month, year))
            line_data["monthly_balance"].append(round(_balance, 2))

            
    return line_data