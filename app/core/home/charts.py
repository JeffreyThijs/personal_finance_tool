import datetime
from flask_login import current_user
from app import cache
from app.tools.dateutils import MONTHS, get_x_prev_months
from app.sqldb.models import Transaction
from app.sqldb.api.v1.prognoses import get_prognosis_data
from app.sqldb.api.v1.transactions import get_user_partial_transactions, QueryPartitionRule, get_user_balance, calculate_balance

@cache.memoize(timeout=300)
def get_donut_charts_data():

    donut_data = {}
    donut_data["labels"] = [c[1] for c in Transaction.TransactionType.choices()]
    donut_data["incoming"] =  [0] * len(donut_data["labels"])
    donut_data["outgoing"] =  [0] * len(donut_data["labels"])

    transactions = get_user_partial_transactions(user_id=current_user.id, start_year=1)

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
def get_bar_charts_data(last_x_months=12):

    bar_data = {"labels" : [0.0] * last_x_months,
                "incoming" : [0.0] * last_x_months,
                "outgoing" : [0.0] * last_x_months,
                "expected_incoming" :  [0.0] * last_x_months,
                "expected_outgoing" :  [0.0] * last_x_months}

    ts = get_user_partial_transactions(user_id=current_user.id, 
                                       partition_rule=QueryPartitionRule.PER_MONTH,
                                       start_year=datetime.datetime.now().year - 1)
    last_ordered_x_months, last_ordered_x_months_year = get_x_prev_months(last_x_months)

    unique_years = list(set(last_ordered_x_months_year))
    prognosis_data = {}
    for year in unique_years:
        prognosis_data[year] = get_prognosis_data(int(year), user_id=current_user.id)

    for i, (month, year) in enumerate(zip(last_ordered_x_months, last_ordered_x_months_year)):
        
        sum_incoming, sum_outgoing = 0.0, 0.0

        if (year in ts) and (month in ts[year]):
            for t in ts[year][month]:
                if t.incoming:
                    sum_incoming += t.price
                else:
                    sum_outgoing += t.price

        bar_data["labels"][i] = "{} {}".format(month, year)
        bar_data["incoming"][i] = round(sum_incoming, 2)
        bar_data["outgoing"][i] = round(sum_outgoing, 2)

        sum_incoming, sum_outgoing = 0.0, 0.0

        if (year in prognosis_data) and (month in prognosis_data[year]):
            sum_incoming += prognosis_data[year][month]["incoming"]
            sum_outgoing += prognosis_data[year][month]["outgoing"]

        bar_data["expected_incoming"][i] = round(sum_incoming, 2)
        bar_data["expected_outgoing"][i] = round(sum_outgoing, 2)

    return bar_data

@cache.memoize(timeout=300)
def get_line_charts_data():
    line_data = {"labels" : [],
                 "monthly_balance" : [],
                 "current_balance" : 0.0}

    line_data["current_balance"] = get_user_balance(current_user.id)
    ts = get_user_partial_transactions(user_id=current_user.id, 
                                       partition_rule=QueryPartitionRule.PER_MONTH,
                                       start_year=1)

    _balance = 0.0
    for year in ts:
        for month in ts[year]:
            _balance += calculate_balance(ts[year][month])
            line_data["labels"].append("{} {}".format(month, year))
            line_data["monthly_balance"].append(round(_balance, 2))
            
    return line_data