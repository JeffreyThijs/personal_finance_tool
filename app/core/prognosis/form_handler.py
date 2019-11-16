from flask_login import current_user, login_required
from app.core.prognosis.forms import PrognosisForm, PrognosisRemovalForm, ChangeDateForm, EditPrognosisForm
from app.tools.dateutils import filter_on_MonthYear, _next_month, _previous_month, generic_datetime_parse, MONTHS, date_time_parse
from app.sqldb.prognoses import add_prognosis
from app.sqldb.models import Prognosis
from app import db
from app.tools.base_form_handler import BaseFormHandler

class FormHandler(BaseFormHandler):
    
    def __init__(self, forms=None):
        _default_forms = {
                           "add_prognosis" : PrognosisForm(),
                        #    "edit_prognosis" : EditPrognosisForm(),
                        # "remove_prognosis" : PrognosisRemovalForm(),
                        # "change_date" : ChangeDateForm() 
                        }
        BaseFormHandler.__init__(self, forms=forms, default_forms=_default_forms)

    @staticmethod
    def _handle_edit_current_prognosis(form : EditPrognosisForm) -> bool:
        raise NotImplementedError
        # if form.prognosis_id.data and form.validate_on_submit():
        #     date = date_time_parse(form.date.data, output_type="datetime")
        #     occurance_type = Prognosis.PrognosisType.coerce(form.category.data)
        #     edit_prognosis(id=form.prognosis_id.data, 
        #                      price=form.price.data,
        #                      comment=form.comment.data,
        #                      occurance_type=occurance_type,
        #                      incoming=form.incoming.data,
        #                      date=date)
        #     return True
        # return False 

    @staticmethod
    def _handle_remove_prognosis_form(form : PrognosisRemovalForm) -> bool:
        raise NotImplementedError
        # if form.remove_prognosis_id.data and form.validate_on_submit():
        #     print(form.remove_prognosis_id.data)
        #     remove_prognosis(id=form.remove_prognosis_id.data)
        #     return True
        # return False

    # @login_required
    @staticmethod
    def _handle_change_date_form(form : ChangeDateForm) -> bool:
        raise NotImplementedError
        # if form.change_date_id.data and form.validate_on_submit():
        #     month, year = form.change_date_id.data.split("-", 1)
        #     current_user.last_date_viewed = current_user.last_date_viewed.replace(day=1, month=int(month), year=int(year))
        #     db.session.add(current_user)
        #     db.session.commit()
        #     return True
        # return False

    @staticmethod
    def _handle_add_new_prognosis_form(form : PrognosisForm):
        if form.validate_on_submit():
            add_new_prognosis(price=form.price.data,
                              date=form.date.data,
                              comment=form.comment.data,
                              category=form.occurance_type.data,
                              incoming=form.incoming.data)
            return True
        return False


    def handle_forms(self) -> bool:

        # # editing current prognosiss
        # if ("edit_prognosis" in self.forms) and self._handle_edit_current_prognosis(self.forms["edit_prognosis"]):
        #     return True  

        # # removing current prognosis
        # elif ("remove_prognosis" in self.forms) and self._handle_remove_prognosis_form(self.forms["remove_prognosis"]):
        #     return True  

        # # change date
        # elif ("change_date" in self.forms) and self._handle_change_date_form(self.forms["change_date"]):
        #     return True  

        # new prognosis
        # elif ("add_prognosis" in self.forms) and self._handle_add_new_prognosis_form(self.forms["add_prognosis"]):
        if ("add_prognosis" in self.forms) and self._handle_add_new_prognosis_form(self.forms["add_prognosis"]):
            return True

        else:
            return False