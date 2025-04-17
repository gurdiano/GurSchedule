import flet as ft 
import datetime

from App.view.model.dividers import row5
from App.view.utility.dicts import isoweek_day
from App.view.utility.colors import *

def _get_date(date, column):
    iso = date.isoweekday()
    weekday = isoweek_day[iso]
    res = column - weekday 
    
    return date + datetime.timedelta(days=res)

def row(father: ft.Container, markers, datepicker, row, col):
    def row_hover(e):
        con = e.control
        con.bgcolor = black_2 if con.bgcolor == black_1 else black_1
        con.update()

    def on_hover(e):
        row_hover(e)
        marker.highlight(e)
        datepicker.display_date(e, container.data['date'])

    marker = None
    for _marker in markers:
        if _marker.data == row: marker = _marker

    col = col + 1

    container = row5(father)
    container.bgcolor = black_1
    container.border = ft.border.all(1, black_0)
    container.on_hover = on_hover
    container.data = {
        'row': row, 
        'column': col, 
        'date': _get_date(datepicker.date, col),
        'time': datetime.time(row, 0)
    }  

    return container    