from App.FrontEnd.Services.entities import Percent, HoldDate, month_english as mm_en


import flet as ft
import datetime

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

def hour (father: ft.Container, hr=None):
    per = Percent(father)
    color = "#868686"

    if hr in (0, 6, 12, 18):
        color = "white"

    if hr < 10: hr = f'0{hr}h'
    else: hr = f'{hr}h'

    text = ft.Text(
        hr,
        size=11,
        color=color
    )

    return ft.Container(
        content=text,
        width=per.set_width() - 2,
        height=per.set_height() / 6,
        bgcolor="#0d0d0d",
        border=ft.Border(
            top=ft.border.BorderSide(1, ft.colors.BLACK), 
            bottom=ft.border.BorderSide(1, ft.colors.BLACK)
        ),
        border_radius=ft.border_radius.all(3),
        alignment=ft.alignment.center
    )

def hours_container (father: ft.Container):
    per = Percent(father)

    return ft.Container(
        width=per.set_width(50),
        height=per.set_height(),
        bgcolor="black"
    )

def icon_container (father: ft.Container, src):
    per = Percent(father)

    svg = ft.Image(
        src=src,
        fit="fill",
    )
    
    return ft.Container(
        content=svg,
        width=per.set_width(50),
        height=per.set_height()
    )

def period(father: ft.Container):
    per = Percent(father)

    return ft.Container(
        width=per.set_width(),
        height=per.set_height()/4,
        bgcolor='white',
        alignment=ft.alignment.center
    )

def wrapper(father: ft.Container):
    per = Percent(father)

    return ft.Container(
        width=per.set_width(),
        height=per.set_height(89.5),
        bgcolor="black"
    )

def side_bar(father: ft.Container):
    per = Percent(father)

    side = ft.Container(
        width=per.set_width(5.7),
        height=per.set_height(),
        bgcolor="black",
        alignment=ft.alignment.center,
    )
    return side

def picker_name(father: ft.Container, title=None, event=None):
    _per = Percent(father)

    _name = ft.Text(
        value=title,
        size=9,
        color=COR_TITULO,
        weight= ft.FontWeight.W_700,
    ) 

    _name_container = ft.Container(
        width= _per.set_width(60),
        height= _per.set_height(),
        alignment= ft.alignment.center,
        content= _name,
        on_click=event,
    )

    return _name_container

def picker_icon(father: ft.Container, event=None):
    _per = Percent(father)

    _icon = ft.Image(
        src= r'App\FrontEnd\Resources\Svg\calendar-regular.svg',
        color=COR_TITULO,
        height= _per.set_height(40)
    )

    _icon_container = ft.Container(
        width= _per.set_width(40),
        height= _per.set_height(),
        alignment= ft.alignment.center_left,
        content= _icon,
        on_click= event,
    )

    return _icon_container

