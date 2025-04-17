from App.FrontEnd.Services.entities import Percent 

import flet as ft


def freetime(father: ft.Container):
    per = Percent(father)

    svg = ft.Image(
        src=r"App\FrontEnd\Resources\Svg\clock-regular-white.svg",
        color="white",
        width=8,
        height=10
    )

    text = ft.Text(
        "8h",
        size=10,
        color="white"
    )

    return ft.Container(    
        content= ft.Row(
            spacing=3,
            wrap=True,

            controls=[
                svg,
                text
            ]
        ),
        width=per.set_width()/7,
        height=per.set_height(),
        bgcolor='black',
        alignment=ft.alignment.center
    )

def sleeptime(father: ft.Container):
    per = Percent(father)

    svg = ft.Image(
        src=r"App\FrontEnd\Resources\Svg\moon-solid-white.svg",
        width=8,
        height=10,
        color="white"
    )

    text = ft.Text(
        "8h",
        size=10,
        color="white"
    )

    return ft.Container(    
        content= ft.Row(
            spacing=3,
            wrap=True,

            controls=[
                svg,
                text
            ]
        ),

        width=per.set_width()/7,
        height=per.set_height(),
        bgcolor='black',
        alignment=ft.alignment.center
    )

def container_wrapper(father: ft.Container):
    per = Percent(father)

    return ft.Container(
        width=per.set_width(),
        height=per.set_height(50),
        bgcolor="black"
    )