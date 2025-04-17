import flet as ft
from App.view.utility.convs import color_grad
from App.view.utility.fontsize import s3
from App.view.utility.colors import black_0

class Task(ft.Container):
    def __init__(self, father, text, icon, gradient=None, color=None):
        super().__init__()
        self.width = father.width
        self.height = father.height
        self.alignment = ft.alignment.center
        self.gradient = gradient
        self.bgcolor = color

        self.content = ft.Row(
            spacing=5,
            wrap=True,
            controls=[icon, text]
        )

       
