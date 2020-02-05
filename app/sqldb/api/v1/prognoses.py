import logging
from datetime import datetime
from app import db, cache
from flask_jwt_extended import current_user
from app.sqldb.models import Prognosis
from app.sqldb.api.v1.helpers.date_querying_helpers import DateQueryHelper, QueryPartitionRule, __MONTHS__
from app.tools.dateutils import convert_to_datetime, date_parse

_dqh = DateQueryHelper(query_class=Prognosis)

# @cache.memoize(timeout=300)
def get_user_prognoses(user_id, order_attr=None, filter_rules=[]):
    return _dqh.get_user_query_objects(user_id=user_id,  
                                       order_attr=order_attr,
                                       filter_rules=filter_rules)

def get_current_user_prognoses(order_rules=None, filter_rules=[]):
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