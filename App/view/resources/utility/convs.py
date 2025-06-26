import datetime
from .dicts import month_english, isoweek_day

def decimal_to_string (_val):
    if _val < 10: _val = f'0{_val}'
    else: _val = f'{_val}'
    return _val

def name_day(num):
    if num == 1 : day = f'{num}st'
    if num == 2 : day = f'{num}nd'
    if num == 3 : day = f'{num}rd'
    if num > 3 : day = f'{num}th'

    return day

def dec_to_string(hr):
    if hr < 10: hr = f'0{hr}h'
    else: hr = f'{hr}h'

    return hr 

def color_grad(color: str):
    color = color.lstrip('#')

    return [
        f'#CC{color}',
        f'#4D{color}',
    ]

def lucidity_color(lucidy, color):
    color = color.lstrip('#')
    return f'#{lucidy}{color}'

def date_str(month, day):
    return f'{month_english[month]} {day}'

def initial_date_week(date):
    temp_time = datetime.time(10)
    date = datetime.datetime.combine(date, temp_time)

    day_week = isoweek_day[date.isoweekday()]
    ini_week = 1 - day_week
    
    ini_date = date + datetime.timedelta(days= ini_week)
    return ini_date.date()

def next_date_week(date):
    temp_time = datetime.time(10)
    date = datetime.datetime.combine(date, temp_time)

    day_week = isoweek_day[date.isoweekday()]
    nxt_week = 8 - day_week
    
    nxt_date = date + datetime.timedelta(days= nxt_week)
    return nxt_date.date()

def back_date_week(date):
    temp_time = datetime.time(10)
    date = datetime.datetime.combine(date, temp_time)

    day_week = isoweek_day[date.isoweekday()]
    nxt_week = 8 - day_week
    
    nxt_date = date - datetime.timedelta(days= nxt_week)
    return nxt_date.date()

def date_between(ini_week, day):
    temp_time = datetime.time(10)
    ini_date = datetime.datetime.combine(ini_week, temp_time)
    end_date = ini_date + datetime.timedelta(days= 6)
    day = datetime.datetime.combine(day, temp_time)
    return True if day >= ini_date and day <= end_date else False

def get_date_by_column(n, ini_week):
    temp_time = datetime.time(10)
    ini_date = datetime.datetime.combine(ini_week, temp_time)

    date = ini_date + datetime.timedelta(days= n-1)
    return date.date()