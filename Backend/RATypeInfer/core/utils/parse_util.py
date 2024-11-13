import pandas as pd
import re
from isodate import parse_duration
from word2number import w2n
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

fmt_list = [
    '%d/%m/%Y',    # '1/01/2020'
    '%d-%b-%y',    # '1-Mar-20'
    '%d %B %Y',
    '%Y.%m.%d',    # '2020.03.01'
    '%B %d, %Y',   # 'March 1, 2020'
    '%Y%m%d',       # '20200301'
    '%Y-%m-%d %H:%M:%S',
    '%m/%d/%Y',
]

def parse_dates(date_str):
    for fmt in fmt_list:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return pd.NaT

def parse_duration_string(duration_str):
    if pd.isna(duration_str):
        return pd.NaT

    duration_str = duration_str.strip()

    # Handle ISO 8601 duration formats
    if re.match(r'^[+-]?P', duration_str, re.IGNORECASE):
        try:
            td = parse_duration(duration_str)
            if isinstance(td, timedelta):
                return pd.Timedelta(td)
            elif isinstance(td, relativedelta):
                # Convert relativedelta to timedelta
                start_date = datetime(2000, 1, 1)
                end_date = start_date + td
                total_seconds = (end_date - start_date).total_seconds()
                return pd.Timedelta(seconds=total_seconds)
            else:
                return pd.NaT
        except Exception:
            return pd.NaT

    # Define units and their equivalent in seconds
    units_in_seconds = {
        'second': 1,
        'seconds': 1,
        'sec': 1,
        's': 1,
        'minute': 60,
        'minutes': 60,
        'min': 60,
        'm': 60,
        'hour': 3600,
        'hours': 3600,
        'hr': 3600,
        'h': 3600,
        'day': 86400,
        'days': 86400,
        'd': 86400,
        'week': 604800,
        'weeks': 604800,
        'w': 604800,
        'month': 2629800,    # Approximate average
        'months': 2629800,
        'mo': 2629800,
        'year': 31557600,    # Approximate average
        'years': 31557600,
        'yr': 31557600,
        'y': 31557600
    }

    # Regular expression to find number-unit pairs
    pattern = r'(?P<sign>[+-]?)\s*(?P<number>\d+(\.\d+)?|[a-zA-Z]+)\s*(?P<unit>[a-zA-Z]*)'

    matches = re.finditer(pattern, duration_str)
    total_seconds = 0
    found = False

    for match in matches:
        found = True
        sign = match.group('sign')
        number_str = match.group('number')
        unit = match.group('unit').lower()

        # Handle numbers written in words
        try:
            number = float(number_str)
        except ValueError:
            try:
                number = w2n.word_to_num(number_str.lower())
            except ValueError:
                return pd.NaT

        if sign == '-':
            number = -number

        # If unit is missing, assume days
        if not unit:
            unit = 'day'

        unit = unit.lower()

        if unit in units_in_seconds:
            total_seconds += number * units_in_seconds[unit]
        else:
            return pd.NaT  # Unknown unit

    if found:
        return pd.Timedelta(seconds=total_seconds)
    else:
        return pd.NaT
