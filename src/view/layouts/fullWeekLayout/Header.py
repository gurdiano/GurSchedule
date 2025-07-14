import flet as ft

from view.resources.utility import dividers
from view.resources.utility import fontsize
from view.resources.utility import colors

from view.resources.utility.convs import name_day

class Header(ft.Row):
    def __init__(self, father, datepicker):
        super().__init__()
        self.father = father
        self.width = self.father.width
        self.height = self.father.height * dividers.ROW1
        self.alignment = ft.alignment.center_left
        self.spacing = 0
        self.datepicker = datepicker

        self.side = ft.Container(
            width=self.width * dividers.COL1,
            height=self.height,
            content=self.datepicker
        )
        
        self.controls=[
            self.side,
            *[self.day_label(n) for n in range(7)]
        ]
        
    def day_label(self, n):
        day_number = n + 1

        text = ft.Text(
            name_day(day_number),
            size=fontsize.S1,
            color=colors.WHITE_1
        )
        return ft.Container(
            width=self.width * dividers.COL2,
            height=self.height,
            bgcolor=colors.BLACK_0,
            content=text,
            alignment=ft.alignment.center,
            data= day_number,
        )