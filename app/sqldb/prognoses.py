from app import db
from app.sqldb.models import Prognosis
from app.tools.dateutils import convert_to_datetime, date_parse
from datetime import datetime
from flask_login import current_user, login_required
from app import cache
import logging
import operator as op

# @cache.memoize(timeout=300)
@login_required
def get_user_prognoses(sort_attr="date", *filter_rules):
    logging.info("Fetching user prognoses ...")
    prognoses_query = current_user.prognoses.filter(*filter_rules)
    return prognoses_query.order_by(op.attrgetter(sort_attr)(Prognosis)).all()

def _add_prognosis(amount : float,
                   date : datetime = None,
                   incoming : bool = False,
                   occurance_type : Prognosis.PrognosisOccuranceType = Prognosis.PrognosisOccuranceType.ONCE,
                   comment : str = "placeholder"):

    prognosis = Prognosis(amount=amount,
                          date=date,
                          incoming=incoming,
                          type=occurance_type,
                          comment=comment,
                          user_id=current_user.id)
    db.session.add(prognosis)
    db.session.commit()

def add_new_prognosis(amount : float,
                      date : str = None,
                      incoming : bool = False,
                      occurance_type : Prognosis.PrognosisOccuranceType = Prognosis.PrognosisOccuranceType.ONCE,
                      comment : str = "placeholder"):

    if date:
        day, month, year = date_parse(date)
        dt = convert_to_datetime(day, month, year)
    else:
        dt = None

    _add_prognosis(amount=amount,
                   date=dt,
                   incoming=incoming,
                   occurance_type=occurance_type,
                   comment=comment)

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