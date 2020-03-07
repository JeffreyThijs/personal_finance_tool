import datetime
from flask_login import current_user
from app.sqldb.models import Prognosis
from app.tools.dateutils import get_days_in_month, month_delta, date_delta
from app.sqldb.api.v1.prognoses import update_last_prognosis_viewed

def transition_yearly_overview(increment : bool):
    last_prognosis_viewed = current_user.last_prognosis_viewed if current_user.last_prognosis_viewed else datetime.datetime.now()
    last_prognosis_viewed = last_prognosis_viewed.replace(year=last_prognosis_viewed.year+1) \
                            if increment else last_prognosis_viewed.replace(year=last_prognosis_viewed.year - 1)
    update_last_prognosis_viewed(last_prognosis_viewed, user=current_user)