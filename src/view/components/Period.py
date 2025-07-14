import flet as ft

from view.resources.utility.dicts import period_color
from view.resources.utility.dicts import period_icon as path

class Period(ft.Container):
    def __init__(self, father, n):
        super().__init__()
        self.father = father
        self.n = n
        self.width = self.father.width
        self.height = self.father.height * 0.25
        self.alignment = ft.alignment.center

        self.svg = ft.Image(
            src=path[self.n],
            fit='fill',
        )
        self.bg = ft.Container(
            width=self.father.width * 0.80,
            height=self.father.height * 0.25,
            content=self.svg,
            alignment=ft.alignment.center,
        )

    def build(self):
        color = period_color[self.n]
        self.bgcolor = color
        self.content = self.bg
        
         


