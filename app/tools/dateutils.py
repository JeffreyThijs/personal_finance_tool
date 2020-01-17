import datetime
from dateutil import relativedelta
import numpy as np
from collections import deque

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
          'august',  'september', 'october', 'november', 'december']

def convert_to_datetime(day: str,
                        month: str,
                        year: str,
                        hour: str = "12",
                        minute: str = "00",
                        second: str = "00") -> datetime:

    date_string_format = "{} {} {} {} {} {}".format(day, month, year,
                                                    hour, minute, second)

    # try normal formal
    try:
        return datetime.datetime.strptime(date_string_format, '%d %m %Y %H %M %S')
    except:
        pass
    # retry reversing day and year
    try:
        return datetime.datetime.strptime(date_string_format, '%Y %m %d %H %M %S')
    except:
        return None

def generic_datetime_parse(dt : datetime, format : str) -> str:
    return dt.strftime(format)

def date_time_parse(date_time : str, 
                   datetime_seperator : str = " ", 
                   date_seperator : str = "-", 
                   time_separator : str = ":",
                   output_type = "tuple",
                   reverse_date = False):

    if (date_seperator not in date_time):
        raise ValueError("date_time string {} does not contain the right seperators")
    
    if time_separator not in date_time:
        return date_parse(date_time, 
                          output_type=output_type,
                          reverse_date=reverse_date)

    if datetime_seperator not in date_time:
        raise ValueError("date_time string {} does not contain the right seperators")
    else:
        date, time = date_time.split(datetime_seperator, 1)
        hour, minute, second = time.split(time_separator, 2)
        if not reverse_date:
            day, month, year = date.split(date_seperator, 2)
        else:
            year, month, day = date.split(date_seperator, 2)
  
    if output_type == "tuple":
        return tuple((day, month, year, hour, minute, second))
    elif output_type == "datetime":
        return convert_to_datetime(day, month, year, hour, minute, second)
    else:
        raise ValueError("unknown output type: {}".format(output_type))

def date_parse(date: str, seperator="-", output_type="tuple", reverse_date = False):
    if seperator not in date:
        raise ValueError( "date {} does not contain seperator {}".format(date, seperator))

    if not reverse_date:
        day, month, year = date.split(seperator, 2)
    else:
        year, month, day = date.split(seperator, 2)

    if output_type == "tuple":
        return tuple((day, month, year))
    elif output_type == "datetime":
        return convert_to_datetime(day, month, year)
    else:
        raise ValueError("unknown output type: {}".format(output_type))

def filter_on_datetime(objects,
                       begin_date: str,
                       end_date: str):

    start_day, start_month, start_year = date_parse(begin_date)
    end_day, end_month, end_year = date_parse(end_date)

    start_dt = convert_to_datetime(start_day, start_month, start_year,
                                   "00", "00", "00")
    end_dt = convert_to_datetime(end_day, end_month, end_year,
                                 "23", "59", "59")

    return list(filter(lambda o: (o.date <= end_dt) and (o.date >= start_dt), objects))

def partition_in_MonthYear(datetime_objects):

    dt_dict = dict()

    for datetime_object in datetime_objects:
        dt = datetime_object.date
        year_str = str(dt.year)
        month_str = MONTHS[dt.month - 1]

        if year_str not in dt_dict:
            dt_dict[year_str] = dict()
        
        if month_str not in dt_dict[year_str]:
            dt_dict[year_str][month_str] = []

        dt_dict[year_str][month_str].append(datetime_object)

    return dt_dict


def filter_on_last_x_months(objects, x_months):

    if not isinstance(x_months, int) or x_months < 1:
        raise ValueError("invalid months")

    start_month = change_month(datetime.datetime.now().month, -x_months + 1)
    year_compensation = 1 if datetime.datetime.now().month < start_month else 0
    start_year = datetime.datetime.now().year - (np.floor((x_months - 1) / 12).astype(int)) - year_compensation
    end_month = datetime.datetime.now().month
    end_year = datetime.datetime.now().year
    
    end_day = str(get_days_in_month(int(end_month), int(end_year)))

    begin_date = "01" + "-" + str(start_month) + "-" + str(start_year)
    end_date = end_day + "-" + str(end_month) + "-" + str(end_year)

    print(begin_date)
    print(end_date)

    return filter_on_datetime(objects=objects,
                              begin_date=begin_date,
                              end_date=end_date)

def get_x_prev_months(x : int):

    if not isinstance(x, int) or x < 0:
        raise ValueError("invalid input")

    current_month = datetime.datetime.now().month
    prev_months = MONTHS * int(1 + (x - 1) / 12)
    prev_years = [0] * x

    # put months in right order
    prev_months = deque(prev_months)
    prev_months.rotate(-current_month)
    prev_months = list(prev_months)

    _year = datetime.datetime.now().year
    for i, month in enumerate(reversed(prev_months)):
        print(month)
        if month == MONTHS[-1]:
            _year -= 1
        prev_years[i] = str(_year)
    prev_years.reverse()

    # only keep last x values
    return prev_months[-x:], prev_years[-x:]


def filter_on_MonthYear(objects,
                        datetime_attr : str,
                        month : str,
                        year : str):

    if month.lower() in MONTHS: month = convert_month(month)
    end_day = str(get_days_in_month(int(month), int(year)))
    begin_date = "01-"+month+"-"+year
    end_date = end_day+"-"+month+"-"+year

    return filter_on_datetime(objects=objects,
                              begin_date=begin_date,
                              end_date=end_date)

def convert_month(month: str) -> str:
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    if is_number(month):
        return MONTHS[int(month)-1]
    elif isinstance(month, str):
        for i, m in enumerate(MONTHS):
            if m == month.lower():
                return str(i+1).zfill(2)
    else:
        raise ValueError("Invalid input")

def change_month(month, offset : int = 0) -> int:
    if isinstance(month, str) and (month.lower() in MONTHS): month = convert_month(month)
    return ((((int(month)-1) + offset) % 12) + 1)

def _previous_month(month : str) -> int:
    return change_month(month, -1)

def _next_month(month : str) -> int:
    return change_month(month, 1)

def get_days_in_month(month: int, year: int) -> int:
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    elif month == 2 and year % 4 == 0:
        return 29
    else:
        return 28

def date_delta(date_1 : datetime.date, date_2 : datetime.date):
    dd = relativedelta.relativedelta(date_1, date_2)
    # dd.year = dd.year if dd.year else 0
    # dd.month = dd.month if dd.month else 0
    # dd.day = dd.day if dd.day else 0
    return dd

def year_delta(date_1 : datetime.date, date_2 : datetime.date):
    return date_delta(date_1, date_2).year

def month_delta(date_1 : datetime.date, date_2 : datetime.date):
    return date_delta(date_1, date_2).months