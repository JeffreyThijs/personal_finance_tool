import datetime

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
    dt = datetime.datetime.strptime(date_string_format, '%d %m %Y %H %M %S')

    return dt

def dt_parse(dt : datetime) -> str:
    return dt.strftime('%B %Y')

def date_time_parse(date_time : str, datetime_seperator=" ", date_seperator="-", time_separator=":") -> tuple:
    if (datetime_seperator not in date_time or 
        date_seperator not in date_time or 
        time_separator not in date_time):
        raise ValueError("date_time string {} does not contain the right seperators")

    date, time = date_time.split(date_time, 1)
    day, month, year = date.split(date_seperator, 2)
    hour, minute, second = time.split(time_separator, 2)
    
    return tuple((day, month, year, hour, minute, second))


def date_parse(date: str, seperator="-") -> tuple:
    if seperator not in date:
        raise ValueError(
            "date {} does not contain seperator {}".format(date, seperator))

    day, month, year = date.split(seperator, 2)

    return tuple((day, month, year))


def filter_on_datetime(objects,
                       datetime_attr: str,
                       begin_date: str,
                       end_date: str):

    start_day, start_month, start_year = date_parse(begin_date)
    end_day, end_month, end_year = date_parse(end_date)

    start_dt = convert_to_datetime(start_day, start_month, start_year,
                                   "00", "00", "00")
    end_dt = convert_to_datetime(end_day, end_month, end_year,
                                 "23", "59", "59")

    return list(filter(lambda o: (getattr(o, datetime_attr) <= end_dt) and
                       (getattr(o, datetime_attr) >= start_dt), objects))


def filter_on_MonthYear(objects,
                        datetime_attr : str,
                        month : str,
                        year : str):

    

    if month.lower() in MONTHS: month = convert_month(month)
    end_day = str(get_days_in_month(int(month), int(year)))
    begin_date = "01-"+month+"-"+year
    end_date = end_day+"-"+month+"-"+year

    return filter_on_datetime(objects=objects,
                              datetime_attr=datetime_attr,
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

def change_month(month : str, offset : int = 0) -> int:
    if month.lower() in MONTHS: month = convert_month(month)
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
