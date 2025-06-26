import flet as ft

from App.view.resources.utility.convs import dec_to_string

from App.view.resources.utility import colors
from App.view.resources.utility import fontsize 
from App.view.resources.utility import dividers

class Marker(ft.Container):
    def __init__(self, controller, page, n):
        super().__init__()
        self.controller = controller
        self.page = page
        self.n = n
        self.clr = colors.WHITE_1 if n in (0, 6, 12, 18) else colors.CTEXT_1
        self.str = dec_to_string(self.n)

        self.width= dividers.MARKER_WIDTH
        self.height= dividers.MARKER_HEIGHT

        self.bgcolor=colors.BLACK_3
        self.alignment=ft.alignment.center
        self.border_radius=ft.border_radius.all(3)

        self.border=ft.Border(
            top=ft.border.BorderSide(1, colors.BLACK_0),
            bottom=ft.border.BorderSide(1, colors.BLACK_0)
        )
        self.txt = ft.Text(
            self.str,
            size=fontsize.S2,
            color=self.clr,
        )
        self.content = self.txt
        self.data = self.n

    def highlight_marker(self, topic, message):
        self.bgcolor = colors.CTHEME_1 if self.bgcolor == colors.BLACK_3 else colors.BLACK_3
        self.update()
        
    
        
        
