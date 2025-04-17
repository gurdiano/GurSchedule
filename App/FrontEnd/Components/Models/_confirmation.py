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

from App.FrontEnd.Services.entities import Percent
import flet as ft


def add_btn(father: ft.Container, event=None):
    per = Percent(father)

    text = ft.Text(
        'Save',
        color=MARK_COLOR,
        size=TITLE_SIZE
    )
    svg = ft.Image(
        src=r'App\FrontEnd\Resources\Svg\sd-card-solid.svg',
        color=ICON_COL0R,
        fit='fill'
    )
    svg_container = ft.Container(
        width=per.set_width(2)+2,
        height=per.set_height(19),
        content=svg,
        alignment=ft.alignment.center,
        padding=ft.padding.only(top=3),
        margin=ft.margin.only(right=per.set_width(6))
    )

    return ft.Container(
        width=per.set_width(27),
        height=per.set_height(50),
        bgcolor='green',
        alignment=ft.alignment.center,
        border_radius=ft.border_radius.all(17),
        border= ft.border.all(1, BORDER_ICON3),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.END,
            spacing=9,
            controls=[
                text,
                svg_container
            ]
        ),
        on_click=event
    )

def confirm_box(father: ft.Container, yes_event=None, no_event=None):
    per = Percent(father)

    text1 = ft.Text(
        'Task discard confirmation.',
        size=MARK_SIZE - 4,
        color=MARK_COLOR,
    )
    text2 = ft.Text(
        'Do you really want to discard this task?',
        size=LABEL_SIZE + 2,
        color=MARK_COLOR,
    )
    buttons = ft.Container(
        padding=ft.padding.only(right=per.set_width(3)),
        content=ft.Row(
            alignment= ft.MainAxisAlignment.END,
            spacing=20,
            controls=[
                ft.TextButton('Yes', on_click=yes_event),
                ft.TextButton('No', on_click=no_event),
            ]
        )
    )
    field1 = ft.Container(
        width=per.set_width(70),
        height=per.set_height(70),
        alignment=ft.alignment.center_left,
        padding=ft.padding.only(left=per.set_width(3)),
        content=text1
    )
    field2 = ft.Container(
        width=per.set_width(70),
        height=per.set_height(70),
        alignment=ft.alignment.center_left,
        padding=ft.padding.only(left=per.set_width(5)),
        content=text2
    )
    field3 = ft.Container(
        width=per.set_width(70),
        height=per.set_height(60),
        alignment=ft.alignment.center,
        content=buttons
    )
    _model = ft.Container(
        width=per.set_width(70),
        height=per.set_height(200),
        bgcolor='black',
        alignment=ft.alignment.center,
        border_radius=ft.border_radius.all(5),
        content=ft.Column(
            spacing=0,
            controls=[
                field1,
                field2,
                field3,
            ]
        )
    )

    return ft.AlertDialog(
        modal=True,
        content=_model,
        bgcolor='#00000000'
    )

def cancel_btn(father: ft.Container=None, event=None):
    per = Percent(father)

    text = ft.Text(
        'Discard',
        color='blue',
        size=TITLE_SIZE,
    )
    
    return ft.Container(
        width=per.set_width(25),
        height=per.set_height(50),
        bgcolor=None,
        alignment=ft.alignment.center,
        border_radius=ft.border_radius.all(17),
        border= ft.border.all(1, BORDER_ICON3),
        content=text,
        on_click=event
    )