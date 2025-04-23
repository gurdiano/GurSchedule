import flet as ft

from App.view.resources.utility.dividers import ROW1, COL1, COL2

from App.view.resources.utility.convs import name_day
from App.view.resources.utility.fontsize import S1
from App.view.resources.utility.colors import WHITE_1, BLACK_0

class Header(ft.Row):
    def __init__(self, father, datepicker):
        super().__init__()
        self.father = father
        self.width = self.father.width
        self.height = self.father.height * ROW1
        self.alignment = ft.alignment.center_left
        self.spacing = 0
        self.datepicker = datepicker

        self.side = ft.Container(
            width=self.width * COL1,
            height=self.height,
            content=self.datepicker
        )
        
    def day_label(self, n):
        text = ft.Text(
            name_day(n + 1),
            size=S1,
            color=WHITE_1
        )

        return ft.Container(
            width=self.width * COL2,
            height=self.height,
            bgcolor=BLACK_0,
            content=text,
            alignment=ft.alignment.center
        )

    def build(self):
        self.controls=[
            self.side,
            *[self.day_label(n) for n in range(7)]
        ]
        
   