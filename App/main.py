import flet as ft

from App.controller.LayoutController import LayoutController

def main(page: ft.Page):
    page.title = "GurSchedule"
    page.padding = 0
    page.window.frameless = True
    
    controller = LayoutController(page)

    #teste field
    from App.controller.TaskController import TaskController

    taskController = TaskController(page)

    page.add(
        ft.WindowDragArea(
            # controller.view.build()
            taskController.taskCreator
        )
    )

ft.app(main)