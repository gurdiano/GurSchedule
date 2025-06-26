from  App.view.AppLayout import AppLayout

from .PickerControler import PickerController
from .MarkerController import MarkerController
from .TableController import TableController
from .TimerController import TimerController
from .taskController import TaskController
from .TitlebarController import TitlebarController
from .BulkController import BulkController

class LayoutController():
    def __init__(self, page):
        self.page = page
        self._sched_queue_size = None
        
        self._initialize_controller()
        self.page.pubsub.subscribe_topic('table-update', self.table_update_handler)
        self.page.pubsub.subscribe_topic('timer-display', self.timer_display_handler)
        self.page.pubsub.subscribe_topic('times-loaded', self.times_loaded_handler)
        self.page.pubsub.subscribe_topic('task-display', self.task_display_handler)
        self.page.pubsub.subscribe_topic('display-new-sched', self.display_new_task_handler)
        self.page.pubsub.subscribe_topic('date-update', self.date_update_handler)
        self.page.pubsub.subscribe_topic('options-click', self.options_click_handler)
        self.page.pubsub.subscribe_topic('picker-value', self.picker_value_handler)
        self.page.pubsub.subscribe_topic('sched-queue', self.sched_queue_handler)
        self.page.pubsub.subscribe_topic('sched-load', self.sched_load_handler)
        self.page.pubsub.subscribe_topic('sched-view-loaded', self.sched_queue_handler)
        self.page.pubsub.subscribe_topic('row-load', self.row_load_handler)
        self.page.pubsub.subscribe_topic('theme-chang', self.theme_chang_handler)
        self.page.pubsub.subscribe_topic('bulk-activated', self.bulk_activated_handler)
        self.page.pubsub.subscribe_topic('copy-bulk', self.copy_bulk_handler)
        self.page.pubsub.subscribe_topic('resize-window', self.resize_window_handler)
        self.page.pubsub.subscribe_topic('row-onclick', self.row_on_click_handler)
        self.page.pubsub.subscribe_topic('scheduler-update', self.scheduler_update_handler)
        

    def _initialize_controller(self):
        self.titlebarController = TitlebarController(self.page)
        self.pickerController = PickerController(self.page)
        self.markerController = MarkerController(self.page)
        self.tableController = TableController(self.page)
        self.timerController = TimerController(self.page)
        self.taskController = TaskController(self.page)
        self.bulkController = BulkController(self.page)
        self.view = AppLayout(self, self.page)
        pass

    def layout_on_load(self):
        if self.titlebarController.changed_theme:
            return self._update_view_theme(self.titlebarController.color_theme)
        self.tableController.date_update_handler('layout_loaded', None)
        pass

    def row_load_handler(self, topic, message):
        self.tableController.row_load_handler(topic, message)
        pass

    def date_update_handler(self, topic, message):
        self.bulkController.date_update_handler(topic, message)
        self.tableController.date_update_handler(topic, message)
        self.tableController.scheds_load_handler(topic, message)
        self.view.date_update(message)
        pass

    def display_new_task_handler(self, topic, message):
        self.view.row_click()
        self.taskController.display_new_task_handler(topic, message)
        pass

    def row_on_click_handler(self, topic, message):
        self.view.row_click()
        self.taskController.row_on_click_handler(topic, message)
        pass

    def options_click_handler(self, topic, message):
        self.view.row_click()
        self.titlebarController.options_click_handler(topic, message)
        pass

    def picker_value_handler(self, topic, message):
        self.pickerController.picker_value_handler(topic, message)
        pass

    def sched_load_handler(self, topic, message):
        self.taskController.sched_load_handler(topic, message)
        pass

    def table_update_handler(self, topic, message):
        self.tableController.table_reload_handler('table_update', None)
        pass

    def timer_display_handler(self, topic, n_column):
        columnsDTO = self.tableController.table_get_columns('timer_display_handler', n_column)
        self.timerController.load_timer_display_handler('timer_display_handler', columnsDTO)
        pass

    def times_loaded_handler(self, topic, message):
        self.timerController.time_values_handler('times_loaded_handler', message)
        self.timerController.load_timer_displays()
        pass

    def task_display_handler(self, topic, message):
        self.view.row_click()
        self.taskController.task_display_handler(topic, message)
        pass

    def sched_queue_handler(self, topic, message):
        if topic == 'sched-queue':
            self._sched_queue_size = message 
        
        if topic == 'sched-view-loaded':
            self._sched_queue_size -= 1

        if self._sched_queue_size == 0: self.titlebarController.times_load_handler(None, None)
        pass

    def resize_window_handler(self, topic, message):
        self.view.toggle()
        pass

    def theme_chang_handler(self, topic, message):
        self._update_view_theme(color= message)
        pass

    def scheduler_update_handler(self, topic, message):
        self._update_view_theme(color= message)
        pass

    def bulk_activated_handler(self, topic, message):
        self.titlebarController.bulk_activated(topic, message)
        pass
    
    def copy_bulk_handler(self, topic, message):
        self.view.row_click()
        self.bulkController.copy_bulk_handler(topic, message)
        pass

    def _update_view_theme(self, color):
        self._initialize_controller()
        self.page.clean()
        self.view.progress_ring(color)
        self.page.add(self.view.build())
        pass

    def titlebar_view(self):
        return self.titlebarController.view

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
