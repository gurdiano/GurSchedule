import flet as ft
from App.view.utility.colors import *
from App.view.utility.fontsize import *
from App.view.model.dividers import col2

def freetime(father: ft.Container):
    container = col2(father)
    container.bgcolor = black_0
    container.alignment = ft.alignment.center

    text = ft.Text(
        '8h',
        color=white_1,
        size= s3
    )
    
    svg = ft.Image(
        src=r'App\view\resource\svg\schedule\clock-regular-white.svg',
        fit='fill',
        color='white',
        width=father.width * 0.25,
        height=father.height * 0.25
    )

    container.content = ft.Row(
        spacing=3,
        wrap=True,

        controls=[
            svg,
            text
        ]
    )

    return container