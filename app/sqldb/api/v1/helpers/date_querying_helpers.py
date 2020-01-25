import datetime
import operator as op
from enum import IntEnum
import numpy as np
from app import db
from app.tools.helpers_classes import AttrDict
from app.tools.dateutils import get_days_in_month

__MONTHS__ = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
              'august',  'september', 'october', 'november', 'december']

class QueryPartitionRule(IntEnum):
    PER_DAY = 1
    PER_WEEK = 2
    PER_MONTH = 3
    PER_YEAR = 4
    PER_DECADE = 5
    NONE = 6

class QueryDate:
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
            if value > 12:
                self._year += int((value-1)/12)
            elif value < 1:
                self._year += np.ceil((value-1)/ 12).astype(int)
            self._month = (((int(value)-1) % 12) + 1)

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value : int):
        if (value is None) or (not isinstance(value, int)):
            self._day = datetime.datetime.now().day
        else:
            if value < 1: value = 1
            if value > get_days_in_month(self.month, self.year): value = get_days_in_month(self.month, self.year)
            self._day = value

class DateQueryHelper:
    def __init__(self, query_class):
        self.query_class = query_class

    def query_object_user_rule(self, user_id):
        return [self.query_class.user_id == user_id]

    def query_object_date_rule(self, start_date : QueryDate, end_date : QueryDate):
        return [self.query_class.date >= start_date.date, self.query_class.date < end_date.date]

    def get_query_objects(self, order_attr="date", *filter_rules):
        return db.session.query(self.query_class).filter(*filter_rules)\
                         .order_by(op.attrgetter(order_attr)(self.query_class))\
                         .all()

    def get_user_query_objects(self, user_id, order_attr=None, filter_rules=[]):
        filter_rules += self.query_object_user_rule(user_id)
        if order_attr is None: order_attr = "date"
        return self.get_query_objects(order_attr, *filter_rules)

    def get_user_partial_query_objects(self, user_id, order_attr=None, partition_rule=None, filter_rules=[], **kwargs):

        start_date = QueryDate(year=kwargs.get("start_year", None),
                               month=kwargs.get("start_month", None),
                               day=kwargs.get("start_day", None))
        end_date = QueryDate(year=kwargs.get("end_year", None),
                             month=kwargs.get("end_month", None),
                             day=kwargs.get("end_day", None))
        
        filter_rules += self.query_object_date_rule(start_date, end_date)

        query_objects = self.get_user_query_objects(user_id=user_id, 
                                                    order_attr=order_attr,
                                                    filter_rules=filter_rules)

        if partition_rule and isinstance(partition_rule, QueryPartitionRule):
            query_objects = self.partition_query_objects_by(query_objects, partition_rule)

        return query_objects

    def partition_query_objects_by(self, query_objects, partition_rule : QueryPartitionRule = QueryPartitionRule.NONE):

        def get_query_objects_dates(query_objects):
            return [QueryDate(year=t.date.year,
                              month=t.date.month,
                              day=t.date.day) for t in query_objects]

        def partion_by_decade(query_objects, query_object_dates):
            query_objects_dict = AttrDict()
            for t, date in zip(query_objects, query_objects_dates): 
                t_decade = str(date.decade)
                if t_decade not in query_objects_dict:
                    query_objects_dict[t_decade] = []
                query_objects_dict[t_decade].append(t)
            return query_objects_dict

        def partion_by_week(query_objects, query_object_dates):
            query_objects_dict = AttrDict()
            for t, date in zip(query_objects, query_objects_dates):
                t_year = str(date.year)
                if t_year not in query_objects_dict:
                    query_objects_dict[t_year] = AttrDict()
                t_week = str(date.week)
                if t_week not in query_objects_dict[t_year]:
                    query_objects_dict[t_year][t_week] = []
                query_objects_dict[t_year][t_week].append(t)
            return query_objects_dict

        def partition_by_year_month_day(query_objects, query_object_dates, partition_rule : QueryPartitionRule):
            query_objects_dict = AttrDict()
            for t, date in zip(query_objects, query_objects_dates):
                t_year = str(date.year)
                if partition_rule.value < QueryPartitionRule.PER_YEAR:
                    if t_year not in query_objects_dict:
                        query_objects_dict[t_year] = AttrDict()
                    t_month = date.smonth
                    if partition_rule.value < QueryPartitionRule.PER_MONTH:
                        if t_month not in query_objects_dict[t_year]:
                            query_objects_dict[t_year][t_month] = AttrDict()
                        t_day = str(date.day)
                        if t_day not in query_objects_dict[t_year][t_month]:
                            query_objects_dict[t_year][t_month][t_day] = []
                        query_objects_dict[t_year][t_month][t_day].append(t)
                    else:
                        if t_month not in query_objects_dict[t_year]:
                            query_objects_dict[t_year][t_month] = []
                        query_objects_dict[t_year][t_month].append(t)
                else:
                    if t_year not in query_objects_dict:
                        query_objects_dict[t_year] = []
                    query_objects_dict[t_year].append(t)
            return query_objects_dict
        
        if partition_rule.value == QueryPartitionRule.NONE:
            return query_objects

        # get query_object dates
        query_objects_dates = get_query_objects_dates(query_objects)

        if partition_rule.value == QueryPartitionRule.PER_DECADE:
            query_objects_dict = partion_by_decade(query_objects, query_objects_dates)
        elif partition_rule.value == QueryPartitionRule.PER_WEEK:
            query_objects_dict.value = partion_by_week(query_objects, query_objects_dates)
        else:
            query_objects_dict = partition_by_year_month_day(query_objects, query_objects_dates, partition_rule)
        
        return query_objects_dict