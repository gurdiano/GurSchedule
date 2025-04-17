from App.FrontEnd.Services.entities import Percent

import flet as ft

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

def beginning(father: ft.Container, hour: ft.Text=None):
    per = Percent(father)

    container_label = ft.Container(
        width=per.set_width(),
        height=per.set_height(20),
        margin=ft.margin.only(left=5),
        alignment=ft.alignment.center_left,
    )
    container_hour = ft.Container(
        width=per.set_width(),
        height=per.set_height(80),
        alignment=ft.alignment.center,
        padding=ft.padding.only(bottom=per.set_height(27))
    )
    label = ft.Text(
        'Beginning:',
        color=LABEL_COLOR,
        size=LABEL_SIZE
    )

    container_label.content = label
    container_hour.content = hour

    return ft.Column(
        spacing=0,
        controls=[
            container_label,
            container_hour
        ]
    )

def day(father: ft.Container, date: ft.Text=None):
    per = Percent(father)

    return ft.Container(
        width=per.set_width(60),
        height=per.set_height(30),
        alignment=ft.alignment.center,
        content=date,
        margin=ft.margin.only(right=per.set_width(25)),
    )

def icon2(father: ft.Container=None, page=None, on_change_date=None):
    def _datepicker(e):
        page.open(
            ft.CupertinoBottomSheet(
                ft.CupertinoDatePicker(
                    date_picker_mode=ft.CupertinoDatePickerMode.DATE_AND_TIME,
                    on_change=on_change_date,
                    use_24h_format=True
                ),

                height=226,
                padding=ft.padding.only(top=6),
            )
        ),
    
    per = Percent(father)

    svg = ft.Image(
        src=r'App\FrontEnd\Resources\Svg\calendar-regular.svg',
        fit='fill',
        color=ICON_COL0R
    )
    svg_container = ft.Container(
        width=per.set_width(17),
        height=per.set_width(17),
        alignment=ft.alignment.center,
        content=svg
    )
    return ft.Container(
        width=per.set_width(ICON_WIDTH),
        height=per.set_height(ICON_HEIGHT),
        alignment=ft.alignment.center,
        border=ft.border.all(1, BORDER_ICON2),
        border_radius=ft.border_radius.all(3),
        content=svg_container,
        bgcolor=BG_ICON_COLOR,
        on_click=_datepicker
    )
