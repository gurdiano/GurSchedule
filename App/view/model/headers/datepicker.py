import flet as ft
import datetime 

from App.view.utility.colors import *
from App.view.utility.fontsize import *
from App.view.utility.dicts import month_english
from App.view.component.DatePicker import DatePicker
from App.view.utility.dicts import isoweek_day


def date_str(month, day):
    return f'{month_english[month]} {day}'

def datepicker(father:ft.Container, table_changer):
    def display_date(e, date):
        act = date_str(picker.date.month, picker.date.day)
        new = date_str(date.month, date.day)

        picker.txt.value = new if picker.txt.value == act else act

        picker.txt.update()

    def on_change(e):
        date = e.control.value
        print(f'date = {date}')
        picker.date = date.date()
        picker.txt.value = date_str(date.month, date.day)

        table_changer(e)
        picker.txt.update()

    def call_datepicker(e):
        _date = date
        _page = picker.page

        _datepicker = ft.DatePicker(
            first_date=datetime.datetime(year=2023, month=1, day=1),
            last_date=datetime.datetime(year=2043, month=1, day=1),
            value=_date,
            on_change=on_change,
        )

        _page.open(
            _datepicker
        )

    picker = DatePicker(father)

    date = datetime.date.today()
    str = date_str(date.month, date.day)
    
    text = ft.Text(
        str,
        size=s4,
        color=theme_1,
        weight=ft.FontWeight.W_700
    )

    svg = ft.Image(
        src=r'App\view\resource\svg\schedule\calendar-regular.svg',
        color=theme_1,
        width=picker.width * 0.40,
        height=picker.height * 0.40,
    )

    picker.content = ft.Row(
        spacing=10,
        wrap=True,
        
        controls=[
            text,
            svg
        ]
    )

    picker.txt = text
    picker.date = date
    picker.display_date = display_date
    picker.on_click = call_datepicker

    return picker

