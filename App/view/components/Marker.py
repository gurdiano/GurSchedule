import flet as ft

from App.view.resources.utility.convs import dec_to_string
from App.view.resources.utility.colors import WHITE_1, CTEXT_1, BLACK_0, BLACK_3, CTHEME_1
from App.view.resources.utility.fontsize import S2

class Marker(ft.Container):
    def __init__(self, controller, page, n):
        super().__init__()
        self.controller = controller
        self.page = page
        self.n = n
        self.clr = WHITE_1 if n in (0, 6, 12, 18) else CTEXT_1
        self.str = dec_to_string(self.n)
        self.width=page.window.width * 0.04
        self.height=page.window.height * 0.03625
        self.bgcolor=BLACK_3
        self.alignment=ft.alignment.center
        self.border_radius=ft.border_radius.all(3)

        self.border=ft.Border(
            top=ft.border.BorderSide(1, BLACK_0),
            bottom=ft.border.BorderSide(1, BLACK_0)
        )
        self.txt = ft.Text(
            self.str,
            size=S2,
            color=self.clr,
        )
        self.content = self.txt
        self.data = self.n

    def highlight_marker(self, topic, message):
        self.bgcolor = CTHEME_1 if self.bgcolor == BLACK_3 else BLACK_3
        self.update()
        
    
        
        
