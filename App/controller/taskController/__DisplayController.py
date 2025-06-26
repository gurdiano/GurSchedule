import flet as ft

from App.view.components.TaskDisplay import TaskDisplay

from App.view.resources.utility import colors, fontsize

from App.dtos.DisplayDTO import DisplayDTO
from App.dtos.RowDTO import RowDTO

from App.model.services import SchedulerService

from App.model.config import get_db

class DisplayController:
    def __init__(self, page):
        self.page = page

    def on_selected_display(self, control, sched_id, dialog):
        self.page.close(dialog)
        displayDTO = DisplayDTO(scheds_id= sched_id, parent= control)
        self.page.pubsub.send_all_on_topic('task-display', displayDTO)
        pass
    
    def on_new_sched(self, control: TaskDisplay, parent):
        data = parent.data
        
        rowDTO = RowDTO(
            n_column= data['column'],
            n_row= data['row'],
            date= data['date'],
            time= data['time'],
            control= control.parent
        )

        self.page.pubsub.send_all_on_topic('display-new-sched', rowDTO)
        pass

    def multitask_on_click(self, control: TaskDisplay):
        scheds_id = control.tasks
        dialog = ft.AlertDialog()

        controls = []
        for sched_id in scheds_id:
            display = self.taskDisplay(sched_id)
            display.set_selected_on_click(control.parent, sched_id, dialog)
            controls.append(display)

        control.open_tasks(controls, dialog)
        pass

    def display_on_click(self, view: TaskDisplay):
        sched_id = view.data
        parent = view.parent

        with get_db() as session:
            schedulerService = SchedulerService(session)
            sched = schedulerService.find(id= sched_id)

            view.tasks.append(sched_id)
            view.times[sched_id] = sched.begin
            
            dialog = ft.AlertDialog()
            display= self.taskDisplay(sched_id)
            display.set_selected_on_click(parent, sched_id, dialog)
            
            view.open_tasks(
                controls= [display],
                dialog= dialog,
            )
            pass

    def created_sched_handler(self, control, scheds_id):
        if len(scheds_id) == 1:
            control.content = self.taskDisplay(sched_id= scheds_id[0])
            self.page.pubsub.send_all_on_topic('sched-view-loaded', None)
            return
            
        with get_db() as session:
            schedulerService = SchedulerService(session)
            
            longest = 0
            scheds = []
            for _id in scheds_id:
                sched = schedulerService.find(id= _id)

                if sched.task.duration >= longest:
                    longest = sched.task.duration
                    scheds.insert(0, sched)
                else:
                    scheds.append(sched)

            longest_sched = scheds.pop(0)
            display = self.taskDisplay(sched_id= longest_sched.id)
            
            for sched in scheds:
                display.add_more_task(
                    sched_id= sched.id,
                    color= sched.priority.color,
                    icon_src= sched.task.icon.src,
                    time= sched.begin
                )

            display.tasks.append(longest_sched.id)
            display.times[longest_sched.id] = longest_sched.begin
            control.content = display

            self.page.pubsub.send_all_on_topic('sched-view-loaded', None)
        pass
       
    def taskDisplay(self, sched_id):
        with get_db() as session:
            schedulerService = SchedulerService(session)

            sched = schedulerService.find(id= sched_id)
            return TaskDisplay(
                controller= self,
                page= self.page,
                title= sched.task.name,
                i_src= sched.task.icon.src,
                color= sched.priority.color,
                data= sched.id
            )