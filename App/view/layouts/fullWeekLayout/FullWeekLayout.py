import flet as ft

from App.view.resources.utility import dividers

from .Header import Header
from .Body import Body
from .Footer import Footer

class FullWeekLayout(ft.Column):
    def __init__(self, app_layout, datepicker, markers, table, freetimers, sleeptimers):
        super().__init__()
        self.app_layout = app_layout

        self.spacing = 0
        self.width = dividers.APP_LAYOUT_WIDTH
        self.height = dividers.APP_LAYOUT_HEIGHT

        self.head = ft.WindowDragArea(
            Header(
                father= self,
                datepicker= datepicker
            ),

            maximizable= False,
        )
        self.body = Body(
            father= self,
            markers= markers,
            table= table
        )
        self.footer = Footer(
            father= self,
            freetimers= freetimers,
            sleeptimers= sleeptimers,
        )
        
        self.controls = [
            self.head,
            self.body,
            self.footer,
        ]

    def did_mount(self):
        self.app_layout.on_load()