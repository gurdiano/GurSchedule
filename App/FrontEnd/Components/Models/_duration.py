from App.FrontEnd.Services.entities import Percent, isoweek_day, month_english as mm_en

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

import datetime

def duration(father: ft.Container, minutes: ft.Text=None):
    per = Percent(father)

    container_label = ft.Container(
        width=per.set_width(),
        height=per.set_height(20),
        margin=ft.margin.only(left=5),
        alignment=ft.alignment.center_left,
    )
    container_duration = ft.Container(
        width=per.set_width(),
        height=per.set_height(80),
        alignment=ft.alignment.center,
        padding=ft.padding.only(bottom=per.set_height(27))
    )
    label = ft.Text(
        'Duration:',
        color=LABEL_COLOR,
        size=LABEL_SIZE
    )
    comp = ft.Container(
        margin=ft.margin.only(top=per.set_height(12)),
        content=ft.Text(
            'minutes',
            color=LABEL_COLOR,
            size=LABEL_SIZE,
        ),
    )

    container_label.content = label
    container_duration.content = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            minutes,
            comp
        ]
    )

    return ft.Column(
        spacing=0,
        controls=[
            container_label,
            container_duration
        ]
    )

def timerpick(time=None, on_change_time=None):
    return ft.TimePicker(
        confirm_text="Confirm",
        error_invalid_text="Time out of range",
        help_text="Pick your time slot",
        on_change=on_change_time,
        time_picker_entry_mode= ft.TimePickerEntryMode.INPUT,
        value=time
    )

def icon3(father: ft.Container, page=None, timerpick=None):
    def _on_click(e):
        page.open(
            timerpick
        )

    per = Percent(father)

    svg = ft.Image(
        src=r'App\FrontEnd\Resources\Svg\clock-regular-white.svg',
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
        on_click=_on_click
    )
