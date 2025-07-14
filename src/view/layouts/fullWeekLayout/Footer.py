import flet as ft 

from view.resources.utility import dividers
from view.resources.utility import colors

class Footer(ft.Container):
    def __init__(self, father, freetimers=None, sleeptimers=None):
        super().__init__()
        self.father = father
        self.width = self.father.width
        self.height = self.father.height * dividers.ROW3
        self.alignment= ft.alignment.center_left

        self.sleeptimers = sleeptimers
        self.freetimers = freetimers

        self.side = ft.Container(
            width=self.width * dividers.COL1,
            height=self.height,
            bgcolor=colors.BLACK_0
        )
        self.timers = ft.Column(
            width=self.father.width * dividers.COL4,
            height=self.father.height * dividers.ROW3,
            spacing=0,   
        )

    def build(self):
        self.timers.controls = [
            ft.Row(spacing=0, controls=self.freetimers),
            ft.Row(spacing=0, controls=self.sleeptimers)
        ]

        self.content = ft.Row(
            spacing=0,
            controls=[
                self.side,
                self.timers
            ]
        )