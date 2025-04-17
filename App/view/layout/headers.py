import flet as ft
from App.view.model.dividers import row1, col1, col2
from App.view.model.headers.day_marker import day_marker


def headers(widget: ft.Container, datepicker):
    header = row1(widget)
    side = col1(header)
    div = col2(header)

    week = [side]
    for n in range(7):
        day = day_marker(div, n)
        week.append(day)

    side.content = datepicker

    header.content = ft.Row(
        spacing=0,

        controls=week
    )    
    return header