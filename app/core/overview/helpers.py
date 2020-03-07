from flask_login import current_user, login_required
from app.tools.dateutils import _next_month, _previous_month, generic_datetime_parse
from app.sqldb.api.v1.transactions import update_last_date_viewed, get_user_monthly_transactions, QueryDate
from app import cache
import time
import datetime

@login_required
def get_current_date_view(format='%B %Y', return_original=False):
    if not current_user.last_date_viewed:
         update_last_date_viewed(datetime.datetime.now(), user=current_user)
    f_current_data = generic_datetime_parse(current_user.last_date_viewed, format=format)
    if return_original:
        return f_current_data, current_user.last_date_viewed
    return f_current_data

# @cache.memoize(timeout=300)
@login_required
def get_months_transactions(last_date_viewed):
    return get_user_monthly_transactions(user_id=current_user.id,
                                         year=last_date_viewed.year,
                                         month=last_date_viewed.month)

def transition_monthly_overview(value : int):
    last_date_viewed = current_user.last_date_viewed if current_user.last_date_viewed else datetime.datetime.now()
    qd = QueryDate(year=last_date_viewed.year,
                   month=last_date_viewed.month,
                   day=last_date_viewed.day)
    qd.month += value
    update_last_date_viewed(qd.date, user=current_user)