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
