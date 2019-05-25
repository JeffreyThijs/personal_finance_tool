from app import db
from app.sqldb.models import Transaction
from app.tools.dateutils import convert_to_datetime, date_parse
from datetime import datetime

def add_new_transaction(price : float,
                        date : str = None,
                        comment : str = "placeholder",
                        user_id : int = None,
                        category : Transaction.TransactionType = Transaction.TransactionType.UNKNOWN,
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
                         category=category,
                         incoming=incoming)

def _add_new_transaction(price : float,
                         comment : str,
                         date : datetime = None,
                         user_id : int = None,
                         category : Transaction.TransactionType = Transaction.TransactionType.UNKNOWN,
                         incoming : bool = False):

    transaction = Transaction(price=price,
                              comment=comment,
                              type=category,
                              incoming=incoming)

    if date: transaction.date = date
    if user_id: transaction.user_id = user_id

    print("Adding new transaction: {}".format(transaction))
    db.session.add(transaction)
    db.session.commit()

def edit_transaction(id : int,
                    price : float = None,
                    comment : str = None,
                    date : datetime = None,
                    user_id : int = None,
                    category : Transaction.TransactionType = None,
                    incoming : bool = None):

    transaction = db.session.query(Transaction).get(id)

    if isinstance(price, float): transaction.price = price
    if isinstance(comment, str): transaction.comment = comment
    if isinstance(date, datetime): transaction.date = date
    if isinstance(user_id, int): transaction.user_id = user_id
    if isinstance(category, Transaction.TransactionType): transaction.category = category
    if isinstance(incoming, bool): transaction.incoming = incoming

    print("Edited transaction: {}".format(transaction))
    db.session.add(transaction)
    db.session.commit()

def remove_transaction(id : int):
    transaction = db.session.query(Transaction).get(id)
    print("Removed transaction: {}".format(transaction))
    db.session.delete(transaction)
    db.session.commit()