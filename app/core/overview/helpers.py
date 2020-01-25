from flask_login import current_user, login_required
from app.tools.dateutils import _next_month, _previous_month, generic_datetime_parse
from app.sqldb.api.v1.transactions import update_last_date_viewed, get_current_user_partial_transactions, QueryPartitionRule, __MONTHS__
from app import cache
import time
import datetime

@login_required
def get_current_date_view(format='%B %Y', return_original=False):
    if not current_user.last_date_viewed:
         update_last_date_viewed(datetime.datetime.now())
    f_current_data = generic_datetime_parse(current_user.last_date_viewed, format=format)
    if return_original:
        return f_current_data, current_user.last_date_viewed
    return f_current_data

# @cache.memoize(timeout=300)
@login_required
def get_months_transactions(last_date_viewed):
    transactions = get_current_user_partial_transactions(partition_rule=QueryPartitionRule.PER_MONTH,
                                                 start_year=last_date_viewed.year,
                                                 end_year=last_date_viewed.year,
                                                 start_month=last_date_viewed.month,
                                                 end_month=last_date_viewed.month+1,
                                                 start_day=1,
                                                 end_day=1)
    syear, smonth = str(last_date_viewed.year), __MONTHS__[last_date_viewed.month - 1]
    return transactions[syear][smonth] if (syear in transactions) and (smonth in transactions[syear]) else []

def transition_monthly_overview(increment : bool):
    last_date_viewed = current_user.last_date_viewed if current_user.last_date_viewed else datetime.datetime.now()
    new_month = _next_month(str(last_date_viewed.month)) if increment else _previous_month(str(last_date_viewed.month))
    last_date_viewed = last_date_viewed.replace(day=1, month=new_month)
    if increment and (last_date_viewed.month == 1):
        last_date_viewed = last_date_viewed.replace(day=1, year=last_date_viewed.year+1)
    elif not increment and (last_date_viewed.month == 12):
        last_date_viewed = last_date_viewed.replace(day=1, year=last_date_viewed.year-1)
    update_last_date_viewed(last_date_viewed)