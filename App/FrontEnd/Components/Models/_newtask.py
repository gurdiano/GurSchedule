from App.FrontEnd.Services.entities import Percent

import flet as ft
import datetime

#Percent
MARGEM_CONTENT = 87
ICON_WIDTH = 90
ICON_HEIGHT = 85

#Colors
ICON_COL0R = '#FFFFFF'
BG_ICON_COLOR = '#101010'
BG_COMP_COLOR = '#000000'
BORDER_ICON1 = '#FFFFFF'
BORDER_ICON2 = '#66000000'
BORDER_ICON3 = '#17ffffff'
BORDER_ICON4 = '#08FFFFFF'
LABEL_COLOR = '#BFFFFFFF'
MARK_COLOR = '#FFFFFF'

#Text
MARK_SIZE = 24
TITLE_SIZE = 17
LABEL_SIZE = 9

def background(father: ft.Container, event=None):
    per = Percent(father)

    return ft.Container(
        width=per.set_width(),
        height=per.set_height(),
        bgcolor='#E6000000',
        on_click=event
    )

def create_task(father: ft.Container):
    per = Percent(father)

    return ft.Container(
        width=per.set_width(45),
        height=per.set_height(85),
        bgcolor='#0a0a0a',
        alignment=ft.alignment.center
    )

def header(father: ft.Container):
    per = Percent(father)

    title = ft.Text(
        'New Task!',
        size=TITLE_SIZE,
        color='white'
    )

    return ft.Container(
        width=per.set_width(),
        height=per.set_height(7),
        bgcolor='#000000',
        alignment=ft.alignment.center,
        content=title
    )

def wrapper(father: ft.Container):
    per = Percent(father)

    return ft.Container(
        width=per.set_width(),
        height=per.set_height(93),
        alignment=ft.alignment.center
    )

def name(father: ft.Container, event=None):
    per = Percent(father)

    tf = ft.TextField(
        label='name',
        border_color=BORDER_ICON1,
        bgcolor=BG_COMP_COLOR,
        on_change=event
    )

    return ft.Container(
        width=per.set_width(60),
        height=per.set_height(75),
        alignment=ft.alignment.center,
        content=tf
    )

def name_container(father: ft.Container):
    per = Percent(father)

    return ft.Container(
        width=per.set_width(MARGEM_CONTENT),
        height=per.set_height(30),
        alignment=ft.alignment.center,
    )

def divider(father: ft.Container):
    per = Percent(father)

    return ft.Container(
        width=per.set_width(MARGEM_CONTENT),
        height=per.set_height(17.5),
        alignment=ft.alignment.center,
        # border=ft.border.all(1, 'red')
    )

def field(father: ft.Container):
    per = Percent(father)

    return ft.Container(
        width=per.set_width(33),
        height=per.set_height(),
        alignment=ft.alignment.center,
        # border=ft.border.all(1, 'orange')
    )

def priority(father: ft.Container):
    per = Percent(father)

    label = ft.Text(
        'Priority:',
        color=LABEL_COLOR,
        size=LABEL_SIZE
    )
    return ft.Container(
        width=per.set_width(),
        height=per.set_height(20),
        margin=ft.margin.only(left=5),
        alignment=ft.alignment.center_left,
        content=label
    )

def grid_icons(father: ft.Container):
    per = Percent(father)
    return ft.Container(
        width=per.set_width(),
        height=per.set_height(80),
        alignment=ft.alignment.center
    )

def icon(father: ft.Container):
    per = Percent(father)

    svg = ft.Image(
        src=r'App\FrontEnd\Resources\Svg\list-check-solid.svg',
        fit='fill',
        color=BORDER_ICON1
    )

    return ft.Container(
        width=per.set_width(5),
        height=per.set_height(20),
        alignment=ft.alignment.center,
        content=svg
    )

def priority_icons(father: ft.Container, color=None, src=None, name=None):
    per = Percent(father)

    svg = ft.Image(
        src=src,
        fit='fill',
        color=ICON_COL0R
    )

    _name = ft.Text(
        name,
        size=9,
        color='white',
        weight=ft.FontWeight.W_300
    )
    svg_container = ft.Container(
        width=per.set_height(47),
        height=per.set_height(47),
        alignment=ft.alignment.center,
        content=svg,
    )
    svg_container_plus = ft.Container(
        width=per.set_height(60),
        height=per.set_height(50),
        alignment=ft.alignment.center,
        content=svg_container,
    )
    name_container = ft.Container(
        width=per.set_height(60),
        height=per.set_height(18),
        content=_name,
        alignment=ft.alignment.center,
    )

    col = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0,
        controls=[
            svg_container_plus,
            name_container
        ]
    )

    if name=='':
        col = svg_container

    return ft.Container(
        width=(per.set_width()-12) / 6 ,
        height=per.set_height(),
        bgcolor=color,
        alignment=ft.alignment.center,
        content=col,
        border=ft.border.all(1, BORDER_ICON4 if name != '' else BORDER_ICON3),
        border_radius=ft.border_radius.all(3)
    )

