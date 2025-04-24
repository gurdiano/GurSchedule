from App.view.components.Table import Table
from App.view.components.TaskDisplay import TaskDisplay
from App.view.components.TaskDetails import TaskDetails

from App.model.services import SchedulerService
from App.model.services import DayService

from . import SESSION

class TableController:
    def __init__(self, page):
        self.page = page
        self.schedService = SchedulerService(SESSION)
        self.dayService = DayService(SESSION)
        self.view = Table(self, page)
        self.page.pubsub.subscribe_topic('dateupdate', self.date_update_handler)    

    def date_update_handler(self, topic, message):
        self.view.rows_date_update(message)
    
    def get_display(self, sched):
        return TaskDisplay(
            page= self.page,
            title= sched.task.name,
            i_src= sched.task.icon.src,
            color= sched.priority.color,
            data= sched
        )

    def search_sched(self, date=None, hour=None):
        day = self.dayService.find(date=date)
        sched = self.schedService.find(day=day, hour=hour)
        if sched: return self.get_display(sched[0])
    
    def update_table(self):
        self.view.load()
        self.view.update()