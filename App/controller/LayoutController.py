from  App.view.AppLayout import AppLayout

from .PickerControler import PickerController
from .MarkerController import MarkerController
from .TableController import TableController
from .TimerController import TimerController
from .taskController import TaskController

class LayoutController():
    def __init__(self, page):
        self.page = page
        self.page.window.width = 1356
        self.page.window.height = 678
        
        self.pickerController = PickerController(page)
        self.markerController = MarkerController(page)
        self.tableController = TableController(page)
        self.timerController = TimerController(page)
        self.taskController = TaskController(page)

        self.view = AppLayout(self, page)

    def layout_on_load(self):
        self.tableController.date_update_handler('layout_loaded', None)
        pass

    def datepicker_view(self):
        return self.pickerController.view
    
    def marker_controls(self):
        return self.markerController.controls
    
    def table_view(self):
        return self.tableController.view
    
    def freetimer_controls(self):
        return self.timerController.freetimers_control
    
    def sleeptimer_controls(self):
        return self.timerController.sleeptimers_control
