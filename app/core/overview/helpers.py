from flask_login import current_user, login_required
from app.tools.dateutils import filter_on_MonthYear, _next_month, _previous_month, generic_datetime_parse
from app.sqldb.dbutils import update_last_date_viewed
from app import cache

@login_required
def get_current_date_view(format='%B %Y', return_original=False):
    f_current_data = generic_datetime_parse(current_user.last_date_viewed, format=format)
    if return_original:
        return f_current_data, current_user.last_date_viewed
    return f_current_data

# @cache.memoize(timeout=300)
@login_required
def get_months_transactions(transactions, last_date_viewed):
    return filter_on_MonthYear(transactions, "date", str(last_date_viewed.month), str(last_date_viewed.year))

def transition_month(increment : bool):
    last_date_viewed = current_user.last_date_viewed
    new_month = _next_month(str(last_date_viewed.month)) if increment else _previous_month(str(last_date_viewed.month))
    last_date_viewed = last_date_viewed.replace(day=1, month=new_month)
    if increment and (last_date_viewed.month == 1):
        last_date_viewed = current_user.last_date_viewed.replace(day=1, year=last_date_viewed.year-1)
    elif not increment and (last_date_viewed.month == 12):
        last_date_viewed = current_user.last_date_viewed.replace(day=1, year=last_date_viewed.year+1)
    update_last_date_viewed(last_date_viewed)