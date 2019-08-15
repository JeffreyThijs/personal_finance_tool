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


def partition_in_MonthYear(objects, 
                           datetime_attr : str):

    object_dict = dict()

    for o in objects:
        dt = getattr(o, datetime_attr)
        year_str = str(dt.year)
        month_str = MONTHS[dt.month - 1]

        if year_str not in object_dict:
            object_dict[year_str] = dict()
        
        if month_str not in object_dict[year_str]:
            object_dict[year_str][month_str] = []

        object_dict[year_str][month_str].append(o)
    return object_dict

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
