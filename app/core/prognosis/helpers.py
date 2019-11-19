from flask_login import current_user
from app.sqldb.prognoses import get_user_prognoses
from app.sqldb.models import Prognosis
import datetime
from app.tools.dateutils import MONTHS, get_days_in_month, month_delta
from app.tools.helpers_classes import AttrDict

MONTHS = [x.capitalize() for x in MONTHS]

def _get_year_data_base():
    year_data = AttrDict()
    rows = MONTHS + ["Totals"]
    for row in rows:
        year_data[row] = AttrDict({"incoming" : 0, 
                                   "outgoing" : 0, 
                                   "balance" : 0,
                                   "tags" : set(),
                                   "prognoses" : set()})
    return year_data

def _prognosis_date_rule(start_year, end_year=None, 
                        start_month=1, end_month=12, 
                        start_day=1, end_day=31,
                        verbose=False):

    end_year = start_year if end_year == None else end_year
    end_day = get_days_in_month(end_month, end_year) if get_days_in_month(end_month, end_year) < end_day else end_day

    start_date = datetime.date(day=start_day, month=start_month, year=start_year)
    end_date = datetime.date(day=end_day, month=end_month, year=end_year) + datetime.timedelta(days=1)

    if verbose:
        print("start: {}, end: {}".format(start_date, end_date))
        # print("start: {}-{}-{}, end: {}-{}-{}".format(start_day, start_month, start_year,
        #                                               end_day, end_month, end_year))

    return [Prognosis.date >= start_date,
            Prognosis.date < end_date]

def _get_only_once_prognosis_data(year_data, year):
    for i, month in enumerate(MONTHS):
        current_month = i + 1
        filter_rules = _prognosis_date_rule(year, start_month=current_month, end_month=current_month)
        filter_rules += [Prognosis.type == Prognosis.PrognosisOccuranceType.ONCE]
        monthly_prognosis = get_user_prognoses("date", *filter_rules)
        for prognosis in monthly_prognosis:
            if prognosis.incoming:
                year_data[month].incoming += prognosis.amount
            else:
                year_data[month].outgoing += prognosis.amount
            year_data[month].prognoses.add(prognosis)
    return year_data

def _get_daily_prognosis_data(year_data, year):

    # TODO

    return year_data

def _get_monthly_prognosis_data(year_data, year):

    filter_rules = _prognosis_date_rule(year)
    filter_rules += [Prognosis.type == Prognosis.PrognosisOccuranceType.MONTHLY]
    prognosis = get_user_prognoses("date", *filter_rules)
    first_day_of_year = datetime.date(day=1, month=1, year=year)

    for p in prognosis:
        delta = month_delta(p.date.date(), first_day_of_year)
        for i, month in enumerate(MONTHS):
            if (delta < 0) or (i >= (delta - 1)):
                if p.incoming:
                    year_data[month].incoming += p.amount
                else:
                    year_data[month].outgoing += p.amount
                year_data[month].prognoses.add(p)

    return year_data

def _get_yearly_prognosis_data(year_data, year):

    for i, month in enumerate(MONTHS):
        current_month = i + 1
        filter_rules = _prognosis_date_rule(start_year=1, end_year=year, 
                                            start_month=1, end_month=current_month,
                                            start_day=1, end_day=31)
        filter_rules += [Prognosis.type == Prognosis.PrognosisOccuranceType.YEARLY]
        yearly_prognosis = get_user_prognoses("date", *filter_rules)
        for prognosis in yearly_prognosis:
            if prognosis.date.month != current_month:
                continue
            if prognosis.incoming:
                year_data[month].incoming += prognosis.amount
            else:
                year_data[month].outgoing += prognosis.amount
            year_data[month].prognoses.add(prognosis)

    return year_data

def _calc_totals(year_data):
    for month in MONTHS:
        year_data[month].balance = year_data[month].incoming - year_data[month].outgoing

    year_data.Totals.incoming = sum([year_data[str(key)].incoming for key in year_data.keys()])
    year_data.Totals.outgoing = sum([year_data[str(key)].outgoing for key in year_data.keys()])
    year_data.Totals.balance = year_data.Totals.incoming - year_data.Totals.outgoing
    return year_data

def get_prognosis_data(year):
    year_data = _get_year_data_base()
    year_data = _get_only_once_prognosis_data(year_data, year)
    year_data = _get_monthly_prognosis_data(year_data, year)
    year_data = _get_yearly_prognosis_data(year_data, year)
    year_data = _calc_totals(year_data)

    return year_data
