import flet as ft

from App.view.layouts.Header import Header
from App.view.layouts.Body import Body
from App.view.layouts.Footer import Footer

class AppLayout:
    def __init__(self, controller, page):
        self.controller = controller
        self.page = page
        
        self.view = ft.Container(
            width=self.page.window.width,
            height=self.page.window.height,
            alignment=ft.alignment.center,
        )
        self.head = Header(
            father=self.view,
            datepicker=self.controller.datepicker_view()
        )
        self.body = Body(
            father=self.view,
            markers=self.controller.marker_controls(),
            table=self.controller.table_view(),
        )
        self.footer = Footer(
            father=self.view,
            freetimers=self.controller.freetimer_controls(),
            sleeptimers=self.controller.sleeptimer_controls(),
        )
    
    def build(self):
        self.view.content = ft.Column(
            spacing=0,
            controls=[
                self.head,
                self.body,
                self.footer
            ]
        )
        return self.view