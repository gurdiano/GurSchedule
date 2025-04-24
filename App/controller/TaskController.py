import flet as ft

from App.view.components.TaskDetails import TaskDetails
from App.view.components.TaskCreator import TaskCreator

from App.model.services import DayService
from App.model.services import SchedulerService
from App.model.services import TaskService
from App.model.services import IconService
from App.model.services import PriorityService
from App.model.exc.IntegrityError import IntegrityError

from . import SESSION

class TaskController:
    def __init__(self, page):
        self.page = page    
        self.details = None

        self.dayService = DayService(SESSION)
        self.schedulerService = SchedulerService(SESSION)
        self.taskService = TaskService(SESSION)
        self.iconService = IconService(SESSION)
        self.priorityService = PriorityService(SESSION)

        self.taskCreator = TaskCreator(self, page)

        self.page.pubsub.subscribe_topic('taskdisplay', self.get_task_details_handler)

    def create_day(self, date):
        try:
            return self.dayService.create(date=date)
        except IntegrityError as e:
            SESSION.rollback()
            return self.dayService.find(date=date)
        
    def create_icon(self, src):
        try:
            return self.iconService.create(src=src)
        except IntegrityError as e:
            SESSION.rollback()
            return self.iconService.find(src=src)

    def create_priority(self, name, color, icon):
        try:
            return self.priorityService.create(
                name=name,
                color=color,
                icon=icon
            )
        except IntegrityError as e:
            SESSION.rollback()
            return self.priorityService.find(name=name)
        
    def create_task(self, name, duration, icon):
        try:
            return self.taskService.create(
                name=name,
                duration=duration,
                icon=icon,
            )
        except IntegrityError as e:
            #raise if person wants update()
            SESSION.rollback()
            return self.taskService.find(name=name, duration=duration)
    
    def create_sched(self, day, priority, task, begin, annotation):
        try:
            return self.schedulerService.create(
                day=day,
                priority=priority,
                task=task,
                begin=begin,
                hour=begin.hour,
                annotation=annotation,
            )
        except IntegrityError as e:
            SESSION.rollback()
            return self.schedulerService.find(day=day, task=task, hour=begin.hour)

    def get_task_details_handler(self, topic, message):
        details = TaskDetails(
            controller= self,
            page= self.page,
            date= message.day.date,
            name= message.task.name,
            begin= message.begin,
            color= message.priority.color,
            priority= message.priority.name,
            duration= message.task.duration,
            icon_src= message.task.icon.src,
            annotation= message.annotation
        )
        self.details = details
        self.page.open(
            details
        )
