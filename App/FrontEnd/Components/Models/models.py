from App.FrontEnd.Components.Models import _wrapperfooter as foot
from App.FrontEnd.Services.entities import Percent

import flet as ft

preto_menos_preto = '#020202'
preto_com_brancodes = '#0a0a0a' 
gelo = '#e0e0e0'
tipo_vinho = '#3c3537'
pink = '#e91e63'
branco = 'white'
verde = '#4caf50'
preto = 'black'

#PICKER
COR_DO_CARD = preto_com_brancodes
COR_DOS_NUM = gelo
COR_TITULO = pink
COR_DA_LINHA = COR_TITULO
COR_SELEÇÃO =  COR_TITULO
SELC_DESTAQUE = branco

#OUTROS
COR_DE_FUNDO = preto
COR_TASK_CON =  preto_menos_preto
HOVER_TASK_CON = preto_com_brancodes


def footer (father: ft.Container):
    per = Percent(father)

    return ft.Container(
        width=per.set_width(),
        height=per.set_height(5.6),
        bgcolor='black'
    )

def header (father: ft.Container, num=None):
    def _name_day(num):
        if num == 1 : day = f'{num}st'
        if num == 2 : day = f'{num}nd'
        if num == 3 : day = f'{num}rd'
        if num > 3 : day = f'{num}th'

        return ft.Text(
            day,
            size=15,
            color='white'
        )
    
    per = Percent(father)
    name = None

    if num is not None:
        name = _name_day(num)
    

    return ft.Container(
        width=per.set_width(),
        height=per.set_height(5),
        bgcolor='black',
        alignment=ft.alignment.center,
        content=name
    )

def wrapper(father: ft.Container):
    per = Percent(father)
    
    return ft.Container(
        width=per.set_width(94.3),
        height=per.set_height(),
        bgcolor="black",
        alignment=ft.alignment.bottom_center,
    )
   
def wrapper_footer(father: ft.Container):
    wrapper_footer = footer(father)
    top_container = foot.container_wrapper(wrapper_footer)
    bot_container = foot.container_wrapper(wrapper_footer)
    
    wrapper_footer.content = ft.Column(
        spacing=0,

        controls=[
            top_container,
            bot_container
        ]
    )

    free_time = []
    sleep_time = []

    for elem in range(7):
        free_time.append(foot.freetime(top_container))

    for elem in range(7):
        sleep_time.append(foot.sleeptime(bot_container))

    top_container.content = ft.Row(
        spacing=0,
        controls=free_time
    )

    bot_container.content = ft.Row(
        spacing=0,
        controls=sleep_time
    )

    return wrapper_footer

def main_content(father: ft.Container):
    per = Percent(father)

    return ft.Container(
        width= per.set_width(),
        height=per.set_height(94.4),
        bgcolor='black'
    )

def task(father: ft.Container, _on_click=None, _on_hover=None):
    _per = Percent(father)

    return ft.Container(
        width=_per.set_width(),
        height=(_per.set_height(95) - 1) / 24,
        bgcolor=COR_TASK_CON,
        alignment=ft.alignment.center,
        border=ft.border.all(1, "black"),
        on_hover=_on_hover,
        on_click=_on_click
    )

def task_content(father: ft.Container, src=None, name=None, priority=None):
    per = Percent(father)

    _task_name = ft.Text(
        name,
        color=ft.colors.WHITE
        )

    return ft.Container(
        width=per.set_width(),
        height=per.set_height(),
        # bgcolor='green',
        alignment=ft.alignment.center,
        content=_task_name
    )

def grade_day(father: ft.Container= None):
    per = Percent(father)

    return ft.Container(
        width=per.set_width()/7,
        height=per.set_height(),
        bgcolor=COR_DE_FUNDO
    )
