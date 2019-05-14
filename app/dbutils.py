from app import db
from app.models import Transaction
from app.tools.dateutils import convert_to_datetime, date_parse
import datetime

def add_new_transaction(price : float,
                        date : str = None,
                        comment : str = "placeholder",
                        user_id : int = None,
                        incoming : bool = False):
    if date:
        day, month, year = date_parse(date)
        dt = convert_to_datetime(day, month, year)
    else:
        dt = None

    _add_new_transaction(price=price,
                         comment=comment,
                         date=dt,
                         user_id=user_id,
                         incoming=incoming)

def _add_new_transaction(price : float,
                         comment : str,
                         date : datetime = None,
                         user_id : int = None,
                         incoming : bool = False):

    transaction = Transaction(price=price,
                              comment=comment,
                              incoming=incoming)

    if date: transaction.date = date
    if user_id: transaction.user_id = user_id

    print("Adding new transaction: {}".format(transaction))
    db.session.add(transaction)
    db.session.commit()