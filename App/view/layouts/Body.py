import flet as ft

from App.view.components.Period import Period
from App.view.resources.utility.dividers import ROW2, COL1, COL3

class Body(ft.Row):
    def __init__(self, father, markers=None, table=None):
        super().__init__()
        self.father = father
        self.width = self.father.width
        self.height = self.father.height * ROW2
        self.spacing=0
        self.markers = markers
        self.table = table

        self.side = ft.Container(
            width= self.width * COL1,
            height= self.height
        )

    def divider(self):
        return ft.Container(
            width= self.side.width * COL3,
            height= self.side.height
        )

    def build(self):
        side = self.side
        f1 = self.divider()
        f2 = self.divider()

        f1.content = ft.Column(
            spacing=0,
            controls=self.markers
        )
        f2.content = ft.Column(
            spacing=0,
            controls=[*[Period(f2, n) for n in range(4)]]
        )
        side.content = ft.Row(
            spacing=0,
            controls=[
                f1,
                f2
            ]
        )

        contents = [side, self.table] if self.table else [side]
        self.controls = contents