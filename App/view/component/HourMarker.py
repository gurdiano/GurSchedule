import flet as ft
from App.view.utility.colors import *

class HourMarker(ft.Container):
    def __init__(self, father, highlight=None):
        super().__init__()

        self.width=father.width * 0.04
        self.height=father.height * 0.03625
        self.highlight = highlight
        self.bgcolor=black_3
        self.alignment=ft.alignment.center
        self.border_radius=ft.border_radius.all(3)
        self.border=ft.Border(
            top=ft.border.BorderSide(1, black_0),
            bottom=ft.border.BorderSide(1, black_0)
            )
    