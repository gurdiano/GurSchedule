from App.view.components import TaskCreator

from App.model.services import SchedulerService
from App.model.services import IconService
from App.model.services import PriorityService

from .. import SESSION

import flet as ft

from App.dtos.SchedDTO import SchedDTO
from App.dtos.RowDTO import RowDTO

class CreatorController:
    def __init__(self, page: ft.Page):
        self.page = page

        self.schedulerService = SchedulerService(SESSION)
        self.iconService = IconService(SESSION)

        self.priorityService = PriorityService(SESSION)

        self.view = TaskCreator(self, page)

    def on_completed(self, data: SchedDTO):
        self.page.pubsub.send_all_on_topic('task-completed', data)
        pass

    def on_creat_priority(self, priority):
        pass

    def on_load_priorities(self):
        self.page.pubsub.send_all_on_topic('load-priorities', 'CreatorController')
    
    def on_selected_task(self, sched_id):
        sched = self.schedulerService.find(id= sched_id)

        if sched:
            schedDTO = self.__schedDTO(sched)
            self.page.pubsub.send_all_on_topic('task-selected', schedDTO)
        pass

    def get_priorities_handler(self, priorities):
        self.view.priority_content.set_options(priorities)
        pass

    def update_priorities_handler(self, priorities):
        self.view.priority_content.set_options(priorities)
        self.view.priority_content.step_update()
        
    def open_creator_handler(self, last_call: RowDTO, data: RowDTO):
        if data:
            date = data.date
            time = data.time
            last_call = last_call.control if last_call else None

            if data.control != last_call:
                self.view.reset(date, time)
                self.page.pubsub.send_all_on_topic('last-call', data)

        def clear_overlay(e):
            self.page.overlay.clear()
            self.page.update()

        self.page.overlay.append(
            ft.Stack(
                alignment= ft.alignment.center,
                
                controls= [
                    ft.Container(
                        bgcolor= '#0d000000',
                        alignment= ft.alignment.center,
                        on_click= clear_overlay,
                    ),
                    
                    self.view,
                ]
            )
        )
        self.page.update()
        pass

    def icon_on_click(self, sched_id):
        sched = self.schedulerService.find(sched_id)
        data = self.__schedDTO(sched)
        self.page.overlay.clear()
        self.get_task_details_handler('icon-onclick', data)

    def _load_icons(self, n):
        items = self.iconService.get_last_items(n)

        res = []
        for item in items:
            res.append(item.src)
        return res
    
    def _load_scheds(self, n, id):
        items = self.schedulerService.get_distinct_last_items(n, id)

        res = []
        for item in items:
            _id  = item.id
            name = item.task.name
            src = item.task.icon.src
            color = item.priority.color

            json = {
                'id' : _id,
                'name' : name,
                'src' : src,
                'color' : color,
            }
            res.append(json)
        return res

    def __schedDTO(self, sched):
        day = sched.day
        task = sched.task
        priority = sched.priority
        icon = task.icon
        
        return SchedDTO(
            icon= icon.src,
            name= task.name,
            date= day.date,
            duration= task.duration,
            time= sched.begin,
            priority= {
                'name': priority.name,
                'src': priority.icon.src,
                'color': priority.color
            },
            annotation= sched.annotation
        )