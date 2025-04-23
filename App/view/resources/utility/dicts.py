from .srcs import DAWN, AFTERNOON, MORNING, NIGHT

isoweek_day = {
    7 : 1,
    1 : 2,
    2 : 3,
    3 : 4,
    4 : 5,
    5 : 6,
    6 : 7,
}

isoweek_day_str = {
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

period_icon = {
    0: DAWN,
    1: AFTERNOON,
    2: MORNING,
    3: NIGHT,
}

period_color = {
    0: '#a6a6a6',
    1: '#fcd5b4',
    2: '#c4d79b',
    3: '#da9694',
}