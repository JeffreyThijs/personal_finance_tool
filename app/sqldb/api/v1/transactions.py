import logging
from datetime import datetime
from app import db, cache
from flask_jwt_extended import current_user
from app.sqldb.models import Transaction
from app.sqldb.api.v1.helpers.date_querying_helpers import DateQueryHelper, QueryPartitionRule, QueryDate, QueryPartitionObject, __MONTHS__
from app.tools.dateutils import convert_to_datetime, date_parse
from typing import List

# typing helper
Transactions = List[Transaction]

_dqh = DateQueryHelper(query_class=Transaction)

# @cache.memoize(timeout=300)
def get_user_transactions(user_id, order_attr=None, filter_rules=[]):
    return _dqh.get_user_query_objects(user_id=user_id,  
                                       order_attr=order_attr,
                                       filter_rules=filter_rules)

def get_current_user_transactions(order_rules=None, filter_rules=[]):
    return get_user_transactions(user_id=current_user.id, 
                                 order_attr=order_rules,
                                 filter_rules=filter_rules)

def get_user_partial_transactions(user_id, order_attr=None, partition_rule=None, return_dict=True, **kwargs):
    return _dqh.get_user_partial_query_objects(user_id=user_id, 
                                               order_attr=order_attr,
                                               partition_rule=partition_rule,
                                               return_dict=return_dict,
                                               filter_rules=[],
                                               **kwargs)

def get_current_user_partial_transactions(order_attr=None, partition_rule=None, return_dict=True, **kwargs):
    return get_user_partial_transactions(user_id=current_user.id,
                                         order_attr=order_attr,
                                         partition_rule=partition_rule,
                                         return_dict=return_dict,
                                         **kwargs)
                
def get_user_monthly_transactions(user_id, year, month, order_attr=None, partition_rule=None, return_dict=True):
    return _dqh.get_query_objects_monthly(user_id=user_id, 
                                          year=year, 
                                          month=month, 
                                          order_attr=order_attr, 
                                          return_dict=return_dict,
                                          partition_rule=partition_rule)

def get_current_user_monthly_transactions(year, month, order_attr=None, partition_rule=None, return_dict=True):
    return get_user_monthly_transactions(user_id=current_user.id,
                                         year=year, 
                                         month=month,
                                         order_attr=order_attr,
                                         return_dict=return_dict, 
                                         partition_rule=partition_rule)

def get_user_yearly_transactions(user_id, year, order_attr=None, partition_rule=None, return_dict=True):
    return _dqh.get_query_objects_yearly(user_id=user_id, 
                                           year=year, 
                                           order_attr=order_attr, 
                                           partition_rule=partition_rule,
                                           return_dict=return_dict)

def get_current_user_yearly_transactions(year, order_attr=None, partition_rule=None, return_dict=True):
    return get_user_yearly_transactions(user_id=current_user.id,
                                        year=year,
                                        order_attr=order_attr, 
                                        partition_rule=partition_rule,
                                        return_dict=return_dict)

def get_current_balance(precision=2):
    transactions = get_current_user_partial_transactions(start_year=1)
    return calculate_balance(transactions, precision=precision)

def calculate_balance(transactions : Transactions,
                      precision : float = 2) -> float:

    profits = sum(t.price for t in transactions if t.incoming)
    losses = sum(t.price for t in transactions if not t.incoming)
    result = round(profits - losses, precision) if precision else (profits - losses)
    return result


def _clear_transaction_cache():
    logging.info("Clearing cached user transactions ...")
    cache.delete_memoized(get_user_transactions)

def add_new_transaction(price : float,
                        date : str = None,
                        comment : str = "placeholder",
                        user_id : int = None,
                        category : Transaction.TransactionType = Transaction.TransactionType.UNKOWN,
                        incoming : bool = False):
    if date:
        day, month, year = date_parse(date)
        date = convert_to_datetime(day, month, year)

    transaction = Transaction(price=price,
                              comment=comment,
                              type=category,
                              incoming=incoming)

    if date: transaction.date = date
    if user_id: transaction.user_id = user_id

    logging.info("Adding new transaction: {}".format(transaction))
    db.session.add(transaction)
    db.session.commit()

    # clear transaction cache on update
    _clear_transaction_cache()

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

    logging.info("Edited transaction: {}".format(transaction))
    db.session.add(transaction)
    db.session.commit()

    # clear transaction cache on update
    _clear_transaction_cache()

def remove_transaction(id : int):
    transaction = db.session.query(Transaction).get(id)
    logging.info("Removed transaction: {}".format(transaction))
    db.session.delete(transaction)
    db.session.commit()

     # clear transaction cache on update
    _clear_transaction_cache()

def update_last_date_viewed(last_date_viewed):
    current_user.last_date_viewed = last_date_viewed
    db.session.add(current_user)
    db.session.commit()