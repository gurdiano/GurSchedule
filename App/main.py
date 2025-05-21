import flet as ft

from App.controller.LayoutController import LayoutController

def main(page: ft.Page):
    page.title = "GurSchedule"
    page.padding = 0
    page.window.frameless = True

    controller = LayoutController(page)

    controller.view.head = ft.WindowDragArea(
        controller.view.head
    )

    page.add(
        controller.view.build()
    )
ft.app(main)