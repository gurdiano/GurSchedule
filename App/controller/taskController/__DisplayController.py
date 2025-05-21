from App.view.components.TaskDisplay import TaskDisplay

from App.dtos.DisplayDTO import DisplayDTO
from App.dtos.SchedDTO import SchedDTO

from App.model.services import SchedulerService

from .. import SESSION

class DisplayController:
    def __init__(self, page):
        self.page = page
        self.schedulerService = SchedulerService(SESSION)

    def display_on_click(self, view: TaskDisplay):
        sched_id = view.data
        parent = view.parent
        return DisplayDTO(sched_id= sched_id, parent= parent)
    
    def created_sched_handler(self, control, sched_id):
        control.content = self.taskDisplay(sched_id= sched_id)
        pass
       
    def taskDisplay(self, sched_id):
        sched = self.schedulerService.find(id= sched_id)
        return TaskDisplay(
            controller= self,
            page= self.page,
            title= sched.task.name,
            i_src= sched.task.icon.src,
            color= sched.priority.color,
            data= sched.id
        )