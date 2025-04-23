import flet as ft

from App.view.resources.utility.colors import BLACK_0, WHITE_1
from App.view.resources.utility.dividers import COL2
from App.view.resources.utility.fontsize import S3

class Timer(ft.Container):
    def __init__(self, controller, page, txt, svg_src):
        super().__init__()
        self.controller = controller
        self.page = page
        self.width = self.page.window.width * COL2
        self.height = self.page.window.height * 0.04
        self.bgcolor = BLACK_0
        self.alignment = ft.alignment.center

        self.text = ft.Text(
            txt,
            color=WHITE_1,
            size=S3
        )

        self.svg = ft.Image(
            src=svg_src,
            fit=ft.ImageFit.CONTAIN,
            color=WHITE_1,
            width=self.height * 0.40,
            height=self.height * 0.40
        )

    def build(self):
        self.content = ft.Row(
            spacing=4,
            wrap=True,

            controls=[
                self.svg,
                self.text
            ]
        )