import flet as ft
from App.view.utility.dicts import period_color
from App.view.utility.dicts import period_icon as path

def period_icon(father: ft.Container, n):
    svg = ft.Image(
        src=path[n],
        fit='fill',
    )
    color = period_color[n]

    bg = ft.Container(
        width=father.width * 0.80,
        height=father.height * 0.25,
        content=svg,
        alignment=ft.alignment.center,
    )

    return ft.Container(
        width=father.width,
        height=father.height * 0.25,
        bgcolor=color,
        content=bg,
        alignment=ft.alignment.center,
    )