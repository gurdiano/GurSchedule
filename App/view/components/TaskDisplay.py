import flet as ft

from App.view.resources.utility.dividers import ROW5, COL2
from App.view.resources.utility.fontsize import S3 
from App.view.resources.utility.colors import BLACK_0, BLACK_3, WHITE_2, CTHEME_1
from App.view.resources.utility.convs import color_grad

from App.dtos.DisplayDTO import DisplayDTO

class TaskDisplay(ft.Container):
    def __init__(self, controller, page, title, i_src, color, data):
        super().__init__()
        self.page = page
        self.controller = controller

        # () = table size
        self.width = (page.window.width * 0.92) * COL2
        self.height = (page.window.height * 0.87) * ROW5
        
        self.title = title
        self.i_src = i_src
        self.color = color
        self.data = data
        self.on_click = self.on_click

    def create_priority_view(self):
        icon = self._create_icon(self.i_src, self.color)
        text = self._create_text(self.title, WHITE_2)

        gradient = ft.LinearGradient(
            begin = ft.alignment.center_right,
            end = ft.alignment.center_left,
            colors = color_grad(self.color),
        )
        self.gradient = gradient
        self.border = ft.border.all(2, self.color)
        return [icon, text]
    
    def create_default_view(self):
        icon = self._create_icon(self.i_src, CTHEME_1)
        text = self._create_text(self.title, WHITE_2)
        self.border = ft.border.all(2, BLACK_3)
        self.bgcolor = self.color
        return [icon, text]

    def build(self):
        controls = self.create_priority_view() if self.color else self.create_default_view()

        self.content = ft.Row(
            spacing=5,
            wrap=True,
            controls=controls
        )
    
    def on_click(self, e):
        self.controller.display_on_click(self)
        pass

    def _create_text(self, title, color):
        return ft.Text(
            title.upper(),
            size=S3,
            color=color,
            weight=ft.FontWeight.W_600
        )
    
    def _create_icon(self, src, color):
        circle = ft.CircleAvatar(
            bgcolor=BLACK_0,
            width=self.height * 0.60,
            height=self.height * 0.60,
        )
        svg = ft.Image(
            src=src,
            fit=ft.ImageFit.CONTAIN,
            width=circle.height * 0.80,
            height=circle.height * 0.80,
            color=color
        )
        border = ft.CircleAvatar(
            bgcolor=color,
            width=circle.height * 1.20,
            height=circle.height * 1.20,
            content=circle
        )
        circle.content = svg
        return border