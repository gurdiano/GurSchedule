import flet as ft
import datetime

from App.view.resources.utility import colors
from App.view.resources.utility import dividers
from App.view.resources.utility import fontsize
from App.view.resources.utility import srcs

class Timer(ft.Container):
    def __init__(self, controller, page, mode, column_n):
        super().__init__()
        self.controller = controller
        self.page = page
        self.mode = mode

        self.column_n = column_n
        self.txt = None
        self.sleep_rows = None
        self.sleep_views = None

        self.width = dividers.TIMER_WIDTH
        self.height = dividers.TIMER_HEIGHT
 
        self.bgcolor = colors.BLACK_0
        self.alignment = ft.alignment.center

    def update_timer(self, value, sleep_rows=None):
        if sleep_rows: self.sleep_rows = sleep_rows
        self.sleep_views = None

        self.txt.value = f'{value}' if value > 9 else f'0{value}'
        self.txt.update()
        pass

    def enable_sleep_view(self, e):
        if self.sleep_rows:
            if self.sleep_views:
                for view in self.sleep_views: 
                    view.visible = False if view.visible == True else True
                    view.update()
                return
            
            self.sleep_views = []
            for row in self.sleep_rows:
                if row.content == None:
                    view = self._sleep_view_build()
                    self.sleep_views.append(view)

                    row.content = view
                    row.update()
            pass
        
    def _sleep_view_build(self):
        return ft.Container(
            bgcolor= colors.BLACK_0,

            content= ft.Row(
                controls=[
                    ft.Image(
                        src= srcs.BED,
                        color= colors.BLACK_3,
                        width= self.height * 0.40,
                        height= self.height * 0.40,
                    ),
                    ft.Text(
                        value= 'SLEEP',
                        size= fontsize.S3,
                        color= colors.BLACK_3,
                    ),
                ],
                alignment= ft.MainAxisAlignment.CENTER,
            ),
        )

    def _text(self, txt):
        return ft.Text(
            txt,
            color= colors.WHITE_1,
            size= fontsize.S3
        )
    
    def _icon(self, src):
        return ft.Image(
            src= src,
            fit= ft.ImageFit.CONTAIN,
            color= colors.WHITE_1,
            width=self.height * 0.40,
            height=self.height * 0.40
        )

    def _control(self, txt, src):
        self.txt = self._text(txt)

        return ft.Row(
            spacing=4,

            controls=[
                self._icon(src),
                self.txt,
            ],

            alignment= ft.MainAxisAlignment.CENTER,
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
        )

    def _sleep_timer_build(self):
        src = srcs.MOON_REGULAR
        txt = 0

        self.content = self._control(txt, src)
    
        def on_click(e):
            self.enable_sleep_view(e)
        
        def on_hover(e):
            con = e.control
            con.bgcolor = colors.BLACK_3 if con.bgcolor == colors.BLACK_0 else colors.BLACK_0
            con.update()

        self.on_click = on_click
        self.on_hover = on_hover
        pass

    def _free_timer_build(self):
        src = srcs.CLOCK_REGULAR
        txt = 0

        self.content = self._control(txt, src)
        pass

    def build(self):
        mode = self.mode.upper()

        if mode == 'SLEEP': self._sleep_timer_build()
        if mode == 'FREE': self._free_timer_build()

        pass