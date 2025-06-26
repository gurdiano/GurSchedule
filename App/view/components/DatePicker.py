import flet as ft

from datetime import date, datetime
from App.view.resources.utility.convs import date_str
from App.view.resources.utility.srcs import CALENDAR_REGULAR

from App.view.resources.utility import colors
from App.view.resources.utility import fontsize
from App.view.resources.utility import dividers

class DatePicker(ft.Container):
    def __init__(self, controller, page):
        super().__init__()
        self.controller = controller
        self.page = page
        self.date = date.today()

        self.width = dividers.DATE_PICKER_WIDTH
        self.height = dividers.DATE_PICKER_HEIGHT

        self.bgcolor = colors.BLACK_2
        self.alignment = ft.alignment.center

        self.txt = ft.Text(
            date_str(self.date.month, self.date.day),
            size=fontsize.S4,
            color=colors.CTHEME_1,
            weight=ft.FontWeight.W_700
        )
        self.svg = ft.Image(
            src=CALENDAR_REGULAR,
            color=colors.CTHEME_1,
            width=self.width * 0.40,
            height=self.height * 0.40,
            fit= ft.ImageFit.CONTAIN,
        )

        self.on_click = self.call_datepicker
        self.content = ft.Row(
            spacing=10,
            controls=[
                self.txt,
                self.svg
            ],
            alignment= ft.MainAxisAlignment.CENTER,
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
        )

    def display_date(self, date):
        act = date_str(self.date.month, self.date.day)
        new = date_str(date.month, date.day)
        self.txt.value = new if self.txt.value == act else act
        self.txt.update()

    def update_display(self, date):
        self.date = date
        self.txt.value = date_str(date.month, date.day)
        self.txt.update()
        pass

    def on_change(self, e):
        date = e.control.value
        self.date = date.date()
        self.txt.value = date_str(date.month, date.day)

        self.txt.update()
        self.controller.date_update(self.date)

    def call_datepicker(self, e):
        _date = self.date
        _page = self.page
        _datepicker = ft.DatePicker(
            first_date=datetime(year=2023, month=1, day=1),
            last_date=datetime(year=2043, month=1, day=1),
            value=_date,
            on_change=self.on_change,
        )
        _page.open(
            _datepicker
        )