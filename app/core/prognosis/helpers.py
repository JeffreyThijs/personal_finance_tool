import datetime
from flask_login import current_user
from app.sqldb.models import Prognosis
from app.tools.dateutils import get_days_in_month, month_delta, date_delta
from app.tools.helpers_classes import AttrDict
from app.sqldb.api.v1.prognoses import get_user_partial_prognoses, update_last_prognosis_viewed
from app.sqldb.api.v1.helpers.date_querying_helpers import QueryPartitionRule
from app.sqldb.api.v1.helpers.date_querying_helpers import __MONTHS__ as MONTHS

def _get_year_data_base():
    year_data = AttrDict()
    rows = MONTHS + ["Totals"]
    for row in rows:
        year_data[row] = AttrDict({"incoming" : 0, 
                                   "outgoing" : 0, 
                                   "balance" : 0,
                                   "prognoses" : set()})
    return year_data

def _get_only_once_prognosis_data(year_data, year_prognoses, year):
    for syear in year_prognoses:
        prognoses = list(filter(lambda x: x.type == Prognosis.PrognosisOccuranceType.ONCE, year_prognoses[syear]))
        for p in prognoses:
            smonth = MONTHS[p.date.month]
            year_data[smonth].prognoses.add(p)
            if p.incoming:  
                year_data[smonth].incoming += p.amount
            else:
                year_data[smonth].outgoing += p.amount

    return year_data

def _get_daily_prognosis_data(year_data, year_prognoses, year):
    for syear in year_prognoses:
        prognoses = list(filter(lambda x: x.type == Prognosis.PrognosisOccuranceType.DAILY, year_prognoses[syear]))
        for p in prognoses:
            month = p.date.month 
            start_month_idx = month-1 if int(syear) == year else 0
            for i in range(start_month_idx, len(MONTHS)):
                smonth = MONTHS[i]
                year_data[smonth].prognoses.add(p)
                days_in_month = (get_days_in_month(i + 1, year) if ((i + 1) != p.date.month)
                                 else (get_days_in_month(i + 1, year) - p.date.day + 1))
                if p.incoming:  
                    year_data[smonth].incoming += (p.amount * days_in_month)
                else:
                    year_data[smonth].outgoing += (p.amount * days_in_month)

    return year_data

def _get_monthly_prognosis_data(year_data, year_prognoses, year):
    for syear in year_prognoses:
        prognoses = list(filter(lambda x: x.type == Prognosis.PrognosisOccuranceType.MONTHLY, year_prognoses[syear]))
        for p in prognoses:
            month = p.date.month 
            start_month_idx = month-1 if int(syear) == year else 0
            for i in range(start_month_idx, len(MONTHS)):
                smonth = MONTHS[i]
                year_data[smonth].prognoses.add(p)
                if p.incoming:  
                    year_data[smonth].incoming += p.amount
                else:
                    year_data[smonth].outgoing += p.amount

    return year_data

def _get_yearly_prognosis_data(year_data, year_prognoses, year):
    for syear in year_prognoses:
        prognoses = list(filter(lambda x: x.type == Prognosis.PrognosisOccuranceType.YEARLY, year_prognoses[syear]))
        for p in prognoses:
            smonth = MONTHS[p.date.month - 1]
            year_data[smonth].prognoses.add(p)
            if p.incoming:  
                year_data[smonth].incoming += p.amount
            else:
                 year_data[smonth].outgoing += p.amount

    return year_data

def get_year_prognosis_data(year):
    return get_user_partial_prognoses(user_id=current_user.id,
                                      partition_rule=QueryPartitionRule.PER_YEAR, 
                                      start_year=1, 
                                      start_month=1, 
                                      start_day=1,
                                      end_year=year+1, 
                                      end_month=1, 
                                      end_day=1)

def _calc_totals(year_data):
    for month in MONTHS:
        year_data[month].balance = round(year_data[month].incoming - year_data[month].outgoing, 2)

    year_data.Totals.incoming = round(sum([year_data[str(key)].incoming for key in year_data.keys()]), 2)
    year_data.Totals.outgoing = round(sum([year_data[str(key)].outgoing for key in year_data.keys()]), 2)
    year_data.Totals.balance = round(year_data.Totals.incoming - year_data.Totals.outgoing, 2)
    return year_data

def get_prognosis_data(year):
    print("getting data from year: {}".format(year))
    year_prognoses = get_year_prognosis_data(year)
    year_data = _get_year_data_base()
    year_data = _get_only_once_prognosis_data(year_data, year_prognoses, year)
    year_data = _get_monthly_prognosis_data(year_data, year_prognoses, year)
    year_data = _get_yearly_prognosis_data(year_data, year_prognoses, year)
    year_data = _get_daily_prognosis_data(year_data, year_prognoses, year)
    year_data = _calc_totals(year_data)

    return year_data

def transition_yearly_overview(increment : bool):
    last_prognosis_viewed = current_user.last_prognosis_viewed if current_user.last_prognosis_viewed else datetime.datetime.now()
    last_prognosis_viewed = last_prognosis_viewed.replace(year=last_prognosis_viewed.year+1) \
                            if increment else last_prognosis_viewed.replace(year=last_prognosis_viewed.year - 1)
    update_last_prognosis_viewed(last_prognosis_viewed)