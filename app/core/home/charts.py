from app.tools.dateutils import filter_on_MonthYear, MONTHS, partition_in_MonthYear, filter_on_last_x_months, get_x_prev_months
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
def get_bar_charts_data(transactions, last_x_months=12):

    bar_data = {"labels" : [0.0] * last_x_months,
                "incoming" : [0.0] * last_x_months,
                "outgoing" : [0.0] * last_x_months,
                "expected_incoming" :  [0.0] * last_x_months,
                "expected_outgoing" :  [0.0] * last_x_months}

    ts = filter_on_last_x_months(transactions, last_x_months)
    ts = partition_in_MonthYear(ts)
    last_ordered_x_months, last_ordered_x_months_year = get_x_prev_months(last_x_months)

    unique_years = list(set(last_ordered_x_months_year))
    prognosis_data = {}
    for year in unique_years:
        prognosis_data[year] = get_prognosis_data(int(year))

    for i, (month, year) in enumerate(zip(last_ordered_x_months, last_ordered_x_months_year)):
        
        sum_incoming, sum_outgoing = 0.0, 0.0

        if (year in ts) and (month in ts[year]):
            for t in ts[year][month]:
                if t.incoming:
                    sum_incoming += t.price
                else:
                    sum_outgoing += t.price

        bar_data["labels"][i] = month + " " + year
        bar_data["incoming"][i] = round(sum_incoming, 2)
        bar_data["outgoing"][i] = round(sum_outgoing, 2)

        sum_incoming, sum_outgoing = 0.0, 0.0

        if (year in prognosis_data) and (month.capitalize() in prognosis_data[year]):
            sum_incoming += prognosis_data[year][month.capitalize()]["incoming"]
            sum_outgoing += prognosis_data[year][month.capitalize()]["outgoing"]

        bar_data["expected_incoming"][i] = round(sum_incoming, 2)
        bar_data["expected_outgoing"][i] = round(sum_outgoing, 2)

    return bar_data

@cache.memoize(timeout=300)
def get_line_charts_data(transactions):

    line_data = {"labels" : [],
                 "monthly_balance" : []}

    line_data["current_balance"] = (sum([t.price for t in transactions if (t.incoming and (t.date < datetime.datetime.now()))]) -
                                    sum([t.price for t in transactions if (not t.incoming and (t.date < datetime.datetime.now()))]))
    line_data["current_balance"] = round(line_data["current_balance"], 2)
    transactions_monthly = partition_in_MonthYear(transactions)

    _balance = 0
    for year in transactions_monthly:
        for month in transactions_monthly[year]:
            _balance += (  sum([t.price for t in transactions_monthly[year][month] if t.incoming]) 
                         - sum([t.price for t in transactions_monthly[year][month] if not t.incoming]))
            line_data["labels"].append("{} {}".format(month, year))
            line_data["monthly_balance"].append(round(_balance, 2))

            
    return line_data