from app import db
from app.sqldb.models import Transaction
from flask_login import current_user
import operator as op
import datetime
from enum import IntEnum
from app.tools.helpers_classes import AttrDict

__MONTHS__ = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
              'august',  'september', 'october', 'november', 'december']

class TransactionPartitionRule(IntEnum):
    PER_DAY = 1
    PER_WEEK = 2
    PER_MONTH = 3
    PER_YEAR = 4
    PER_DECADE = 5
    NONE = 6

class TransactionDate:
    def __init__(self, year=None, month=None, day=None):
        self.year = year
        self.month = month
        self.day = day

    def __str__(self):
        return "day: {}, month: {}, year: {}".format(self.day, self.month, self.year)

    @property
    def date(self):
        return datetime.date(year=self._year,
                             month=self._month,
                             day=self._day)
    @property
    def week(self):
        return self.date.isocalendar()[1]

    @property
    def decade(self):
        return int(int(self._year / 10) * 10)

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value : int):
        if (value is None) or (not isinstance(value, int)):
            self._year = datetime.datetime.now().year
        else:
            self._year = value

    @property
    def month(self):
        return self._month

    @property
    def smonth(self):
        return __MONTHS__[self.month - 1]

    @month.setter
    def month(self, value : int):
        if (value is None) or (not isinstance(value, int)):
            self._month = datetime.datetime.now().month
        else:
            self._month = value

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value : int):
        if (value is None) or (not isinstance(value, int)):
            self._day = datetime.datetime.now().day
        else:
            self._day = value

def transaction_user_rule(user_id):
    return [Transaction.user_id == user_id]

def transaction_date_rule(start_date : TransactionDate, end_date : TransactionDate):
    return [Transaction.date >= start_date.date, Transaction.date < end_date.date]

def get_transactions(order_attr="date", *filter_rules):
    return current_user.transactions.filter(*filter_rules)\
                     .order_by(op.attrgetter(order_attr)(Transaction))\
                     .all()

def get_user_transactions(user_id, order_attr=None, filter_rules=[]):
    filter_rules += transaction_user_rule(user_id)
    if order_attr is None: order_attr = "date"
    return get_transactions(order_attr, *filter_rules)

def get_current_user_transactions(user_id, order_rules=None, filter_rules=[]):
    return get_user_transactions(user_id=current_user.id, 
                                 order_attr=order_rules,
                                 filter_rules=filter_rules)

def get_user_partial_transactions(user_id, order_attr=None, partition_rule=None, **kwargs):

    start_date = TransactionDate(year=kwargs.get("start_year", None),
                                 month=kwargs.get("start_month", None),
                                 day=kwargs.get("start_day", None))
    end_date = TransactionDate(year=kwargs.get("end_year", None),
                               month=kwargs.get("end_month", None),
                               day=kwargs.get("end_day", None))
    
    print("start: {} end: {}".format(start_date.date, end_date.date))
    filter_rules = transaction_date_rule(start_date, end_date)

    transactions = get_user_transactions(user_id=user_id, 
                                         order_attr=order_attr,
                                         filter_rules=filter_rules)

    if partition_rule and isinstance(partition_rule, TransactionPartitionRule):
        transactions = partition_transactions_by(transactions, partition_rule)

    return transactions

def get_current_user_partial_transactions(order_attr=None, partition_rule=None, **kwargs):
    return get_user_partial_transactions(user_id=current_user.id,
                                         order_attr=order_attr,
                                         partition_rule=partition_rule,
                                         **kwargs)

def partition_transactions_by(transactions, partition_rule : TransactionPartitionRule = TransactionPartitionRule.NONE):

    def get_transactions_dates(transactions):
        return [TransactionDate(year=t.date.year,
                                month=t.date.month,
                                day=t.date.day) for t in transactions]

    def partion_by_decade(transactions, transaction_dates):
        transactions_dict = AttrDict()
        for t, date in zip(transactions, transactions_dates): 
            t_decade = str(date.decade)
            if t_decade not in transactions_dict:
                transactions_dict[t_decade] = []
            transactions_dict[t_decade].append(t)
        return transactions_dict

    def partion_by_week(transactions, transaction_dates):
        transactions_dict = AttrDict()
        for t, date in zip(transactions, transactions_dates):
            t_year = str(date.year)
            if t_year not in transactions_dict:
                transactions_dict[t_year] = AttrDict()
            t_week = str(date.week)
            if t_week not in transactions_dict[t_year]:
                transactions_dict[t_year][t_week] = []
            transactions_dict[t_year][t_week].append(t)
        return transactions_dict

    def partition_by_year_month_day(transactions, transaction_dates, partition_rule : TransactionPartitionRule):
        transactions_dict = AttrDict()
        for t, date in zip(transactions, transactions_dates):
            t_year = str(date.year)
            if partition_rule.value < TransactionPartitionRule.PER_YEAR:
                if t_year not in transactions_dict:
                    transactions_dict[t_year] = AttrDict()
                t_month = date.smonth
                if partition_rule.value < TransactionPartitionRule.PER_MONTH:
                    if t_month not in transactions_dict[t_year]:
                        transactions_dict[t_year][t_month] = AttrDict()
                    t_day = str(date.day)
                    if t_day not in transactions_dict[t_year][t_month]:
                        transactions_dict[t_year][t_month][t_day] = []
                    transactions_dict[t_year][t_month][t_day].append(t)
                else:
                    if t_month not in transactions_dict[t_year]:
                        transactions_dict[t_year][t_month] = []
                    transactions_dict[t_year][t_month].append(t)
            else:
                if t_year not in transactions_dict:
                    transactions_dict[t_year] = []
                transactions_dict[t_year].append(t)
        return transactions_dict
    
    if partition_rule.value == TransactionPartitionRule.NONE:
        return transactions

    # get transaction dates
    transactions_dates = get_transactions_dates(transactions)

    if partition_rule.value == TransactionPartitionRule.PER_DECADE:
        transactions_dict = partion_by_decade(transactions, transactions_dates)
    elif partition_rule.value == TransactionPartitionRule.PER_WEEK:
        transactions_dict.value = partion_by_week(transactions, transactions_dates)
    else:
        transactions_dict = partition_by_year_month_day(transactions, transactions_dates, partition_rule)
       
    return transactions_dict