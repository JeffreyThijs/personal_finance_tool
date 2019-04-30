import datetime

def convert_to_datetime(day : str,
                        month : str,
                        year : str,
                        hour : str = "12",
                        minute : str = "00",
                        second : str = "00") -> datetime:


    date_string_format = "{} {} {} {} {} {}".format(day, month, year,
                                                    hour, minute, second)
    dt = datetime.datetime.strptime(date_string_format, '%d %m %Y %H %M %S')

    return dt
