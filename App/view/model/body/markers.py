import flet as ft
from App.view.utility.colors import *
from App.view.utility.fontsize import *
from App.view.utility.convs import dec_to_string

from App.view.model.dividers import row5
from App.view.component.HourMarker import HourMarker

def hour_marker(father: ft.Container, n):
    def highlight(e):
            con.bgcolor = theme_1 if con.bgcolor == black_3 else black_3
            con.update()

    color = white_1 if n in (0, 6, 12, 18) else co_text_1
    str = dec_to_string(n)

    text = ft.Text(
        str,
        size=s2,
        color=color,
    )

    con = HourMarker(father)
    con.content = text
    con.data = n
    con.highlight = highlight
    
    return con

def markers(father: ft.Container):
    list = []
    
    for n in range(24):
        marker = hour_marker(father, n)
        list.append(marker)

    return list