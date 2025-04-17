import flet as ft
from App.view.model.dividers import row3, row4, col1, col4
from App.view.model.footers.freetime import freetime
from App.view.model.footers.sleeptime import sleeptime
from App.view.utility.colors import *


def footers(widget: ft.Container):
    footer = row3(widget)

    side = col1(footer)
    cont = col4(footer)

    f1 = row4(cont)
    f2 = row4(cont)

    side.bgcolor = black_0

    ftimes = []
    for n in range(7):
        ftime = freetime(footer)
        ftimes.append(ftime)
    
    stimes = []
    for n in range(7):
        stime = sleeptime(footer)
        stimes.append(stime)

    f1.content = ft.Row(
        spacing=0,
        controls=ftimes
    )

    f2.content = ft.Row(
        spacing=0,
        controls=stimes
    )

    cont.content = ft.Column(
        spacing=0,

        controls=[
            f1,
            f2
        ]
    )

    footer.content = ft.Row(
        spacing=0,

        controls=[
            side,
            cont
        ]
    )

    return footer