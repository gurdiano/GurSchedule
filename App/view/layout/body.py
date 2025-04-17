import flet as ft

from App.view.model.dividers import row2, row5, col1, col3
from App.view.model.body.period_icon import period_icon

def body(widget: ft.Container, markers, table):
    _body = row2(widget)

    side = col1(_body)
    f1 = col3(side)
    f2 = col3(side)

    icons = []
    for n in range(4):
        icon = period_icon(f2, n)
        icons.append(icon)

    f1.content = ft.Column(
        spacing=0,

        controls=markers
    )

    f2.content = ft.Column(
        spacing=0,

        controls= icons
    )

    side.content = ft.Row(
        spacing=0,

        controls=[
            f1,
            f2
        ]
    )

    _body.content = ft.Row(
        spacing=0,

        controls=[
            side,
            table
        ]
    )

    return _body

