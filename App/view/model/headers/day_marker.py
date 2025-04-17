import flet as ft

from utility.colors import *
from utility.fontsize import *
from utility.convs import name_day

def day_marker(father: ft.Container, n):
    day = name_day(n+1)

    text = ft.Text(
        day,
        size=s1,
        color=white_1
    )

    return ft.Container(
        width=father.width,
        height=father.height,
        bgcolor=black_0,
        content=text,
        alignment=ft.alignment.center
    ) 