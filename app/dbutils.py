from app import db
from app.models import Transaction
import datetime

def add_new_transaction(price, comment, date : datetime = None):

    transaction = Transaction(price=price, comment=comment)
    if date: transaction.date = date
    print("Adding new transaction: {}".format(transaction))
    db.session.add(transaction)
    db.session.commit()
