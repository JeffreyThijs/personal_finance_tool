from flask_login import current_user, login_required
from app.core.overview.forms import TransactionForm, TransactionRemovalForm, ChangeDateForm, EditTransactionForm
from app.tools.dateutils import filter_on_MonthYear, _next_month, _previous_month, generic_datetime_parse, MONTHS, date_time_parse
from app.sqldb.dbutils import add_new_transaction, edit_transaction, remove_transaction
from app.sqldb.models import User, Transaction
from app import db

class FormHandler:
    def __init__(self, forms=None):
        self._default_forms = {
            "add_transaction" : TransactionForm(),
            "edit_transaction" : EditTransactionForm(),
            "remove_transaction" : TransactionRemovalForm(),
            "change_date" : ChangeDateForm()
        }
        self._forms = forms if forms is not None else self._default_forms

    @property
    def default_forms(self):
        return self.default_forms

    @default_forms.setter
    def default_forms(self, value):
        raise Exception("Cant change the default forms")

    @property
    def forms(self):
        return self._forms

    @forms.setter
    def forms(self, value):
        self._forms = self.default_forms if not isinstance(value, dict) else value

    @staticmethod
    def _handle_edit_current_transaction(form : EditTransactionForm) -> bool:
        if form.transaction_id.data and form.validate_on_submit():
            date = date_time_parse(form.date.data, output_type="datetime")
            category = Transaction.TransactionType.coerce(form.category.data)
            edit_transaction(id=form.transaction_id.data, 
                             price=form.price.data,
                             comment=form.comment.data,
                             category=category,
                             incoming=form.incoming.data,
                             date=date)
            return True
        return False 

    @staticmethod
    def _handle_remove_transaction_form(form : TransactionRemovalForm) -> bool:
        if form.remove_transaction_id.data and form.validate_on_submit():
            print(form.remove_transaction_id.data)
            remove_transaction(id=form.remove_transaction_id.data)
            return True
        return False

    # @login_required
    @staticmethod
    def _handle_change_date_form(form : ChangeDateForm) -> bool:
        if form.change_date_id.data and form.validate_on_submit():
            month, year = form.change_date_id.data.split("-", 1)
            current_user.last_date_viewed = current_user.last_date_viewed.replace(day=1, month=int(month), year=int(year))
            db.session.add(current_user)
            db.session.commit()
            return True
        return False

    @staticmethod
    def _handle_add_new_transaction_form(form : TransactionForm):
        if form.validate_on_submit():
            add_new_transaction(price=form.price.data,
                                date=form.date.data,
                                comment=form.comment.data,
                                category=form.category.data,
                                user_id=current_user.id,
                                incoming=form.incoming.data)
            return True
        return False


    def handle_forms(self) -> bool:

        # editing current transactions
        if ("edit_transaction" in self.forms) and self._handle_edit_current_transaction(self.forms["edit_transaction"]):
            return True  

        # removing current transaction
        elif ("remove_transaction" in self.forms) and self._handle_remove_transaction_form(self.forms["remove_transaction"]):
            return True  

        # change date
        elif ("change_date" in self.forms) and self._handle_change_date_form(self.forms["change_date"]):
            return True  

        # new transaction
        elif ("add_transaction" in self.forms) and self._handle_add_new_transaction_form(self.forms["add_transaction"]):
            return True

        else:
            return False