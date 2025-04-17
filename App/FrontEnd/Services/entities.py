class HoldDate:
    def __init__ (self, date):
        self.date = date

class Percent:
    def __init__ (self, window):
        self.window = window

    def set_width (self, per=None):
        if per is not None:
            return (per * self.window.width) / 100    
        return self.window.width
    
    def set_height (self, per=None):
        if per is not None:
            return (per * self.window.height) / 100    
        return self.window.height

isoweek_day = {
    0 : 'Mon',
    1 : 'Tue',
    2 : 'Wed',
    3 : 'Thu',
    4 : 'Fri',
    5 : 'Sat',
    6 : 'Sun',
}

month_english = {
    1 : 'Jan',
    2 : 'Feb',
    3 : 'Mar',
    4 : 'Apr',
    5 : 'May',
    6 : 'Jun',
    7 : 'Jui',
    8 : 'Aug',
    9 : 'Sep',
    10 : 'Oct',
    11 : 'Nov',
    12 : 'Dec',
}

def decimal_tostring (_val):
        if _val < 10: _val = f'0{_val}'
        else: _val = f'{_val}'
        return _val