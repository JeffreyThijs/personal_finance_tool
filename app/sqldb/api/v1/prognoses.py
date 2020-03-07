import logging
from datetime import datetime
from app import db, cache
from flask_jwt_extended import current_user
from app.sqldb.models import Prognosis
from app.sqldb.api.v1.helpers.date_querying_helpers import DateQueryHelper, QueryPartitionRule, __MONTHS__
from app.tools.dateutils import convert_to_datetime, date_parse
from app.tools.helpers_classes import AttrDict
from app.tools.dateutils import get_days_in_month

_dqh = DateQueryHelper(query_class=Prognosis)

# @cache.memoize(timeout=300)
def get_user_prognoses(user_id, order_attr=None, filter_rules=None):
    return _dqh.get_user_query_objects(user_id=user_id,  
                                       order_attr=order_attr,
                                       filter_rules=filter_rules)

def get_current_user_prognoses(order_rules=None, filter_rules=None):
    return get_user_prognoses(user_id=current_user.id, 
                              order_attr=order_rules,
                              filter_rules=filter_rules)

def get_user_partial_prognoses(user_id, order_attr=None, partition_rule=None, occurrence_type=None, **kwargs):

    filter_rules = []
    if occurrence_type:
        filter_rules += [Prognosis.type == occurrence_type]

    return _dqh.get_user_partial_query_objects(user_id=user_id, 
                                               order_attr=order_attr,
                                               partition_rule=partition_rule,
                                               filter_rules=filter_rules,
                                               **kwargs)

def get_current_user_partial_prognoses(order_attr=None, partition_rule=None, occurrence_type=None, **kwargs):
    return get_user_partial_prognoses(user_id=current_user.id,
                                      order_attr=order_attr,
                                      partition_rule=partition_rule,
                                      occurrence_type=occurrence_type,
                                      **kwargs)

def get_user_monthly_prognoses(user_id, year, month, order_attr=None, partition_rule=None):
    return _dqh.get_query_objects_monthly(user_id=user_id, 
                                          year=year, 
                                          month=month, 
                                          order_attr=order_attr, 
                                          partition_rule=partition_rule)

def get_current_user_monthly_prognoses(year, month, order_attr=None, partition_rule=None):
    return get_user_monthly_prognoses(user_id=current_user.id,
                                      year=year, 
                                      month=month,
                                      order_attr=order_attr, 
                                      partition_rule=partition_rule)

def add_new_prognosis(amount : float,
                      date : str = None,
                      incoming : bool = False,
                      occurance_type : Prognosis.PrognosisOccuranceType = Prognosis.PrognosisOccuranceType.ONCE,
                      comment : str = "placeholder"):

    if date:
        day, month, year = date_parse(date)
        date = convert_to_datetime(day, month, year)

    prognosis = Prognosis(amount=amount,
                          date=date,
                          incoming=incoming,
                          type=occurance_type,
                          comment=comment,
                          user_id=current_user.id)
    db.session.add(prognosis)
    db.session.commit()

def edit_prognosis(id : int,
                   amount : float = None,
                   comment : str = None,
                   date : datetime = None,
                   user_id : int = None,
                   occurance : Prognosis.PrognosisOccuranceType = None,
                   incoming : bool = None):

    prognosis = db.session.query(Prognosis).get(id)

    if isinstance(amount, float): prognosis.amount = amount
    if isinstance(comment, str): prognosis.comment = comment
    if isinstance(date, datetime): prognosis.date = date
    if isinstance(user_id, int): prognosis.user_id = user_id
    if isinstance(occurance, Prognosis.PrognosisOccuranceType): prognosis.occurance = occurance
    if isinstance(incoming, bool): prognosis.incoming = incoming

    logging.info("Edited prognosis: {}".format(prognosis))
    db.session.add(prognosis)
    db.session.commit()

    # clear prognosis cache on update
    # _clear_prognosis_cache()

def update_last_prognosis_viewed(last_prognosis_viewed):
    current_user.last_prognosis_viewed = last_prognosis_viewed
    db.session.add(current_user)
    db.session.commit()


def _get_year_data_base():
    year_data = AttrDict()
    rows = __MONTHS__ + ["Totals"]
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
            smonth = __MONTHS__[p.date.month-1]
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
            for i in range(start_month_idx, len(__MONTHS__)):
                smonth = __MONTHS__[i]
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
            for i in range(start_month_idx, len(__MONTHS__)):
                smonth = __MONTHS__[i]
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
            smonth = __MONTHS__[p.date.month - 1]
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
    for month in __MONTHS__:
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