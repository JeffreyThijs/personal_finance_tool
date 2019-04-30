from app import db
from app.models import Transaction

def add_new_transaction(price, comment):
    transaction = Transaction(price=price, comment=comment)
    print("Adding new transaction: {}".format(transaction))
    db.session.add(transaction)
    db.session.commit()
