import flet as ft

from App.view.components.TaskDetails import TaskDetails

from App.model.exc.IntegrityError import IntegrityError
from App.model.exc.UnknownError import UnknownError
from App.model.exc.NoFreeTime import NoFreeTime
from App.model.exc.TaskConflicted import TaskConflicted

from App.model.services import DayService
from App.model.services import PriorityService
from App.model.services import IconService
from App.model.services import TaskService
from App.model.services import SchedulerService

from App.dtos.SchedDTO import SchedDTO

from .. import SESSION

class DetailsController:
    def __init__(self, page):
        self.page = page

        self.dayService = DayService(SESSION)
        self.priorityService = PriorityService(SESSION)
        self.iconService = IconService(SESSION)
        self.taskService = TaskService(SESSION)
        self.schedulerService = SchedulerService(SESSION)
        
        self.view = TaskDetails(self, page)

    def get_priorities_handler(self, priorities):
        self.view.set_options(priorities)
        self.view.dropdown.options = self.view.options
        self.view.dropdown.update()

    def on_back_action(self):
        self.page.overlay.clear()
        self.page.pubsub.send_all_on_topic('row-onclick', None)
        pass

    def on_save_sched(self, data: SchedDTO):
        date = data.date
        name = data.name
        icon_src = data.icon
        duration = data.duration
        priority = data.priority
        time = data.time
        annotation = data.annotation
        
        try:
            day = self.__get_day(date)
            priority = self.__get_priority(priority)
            task = self.__get_task(name, duration, icon_src)
            hour = time.hour
            
            sched = self.__get_sched(
                day= day,
                priority= priority,
                task= task,
                hour= hour,
                begin= time,
                annotation= annotation,
            )
            self.page.pubsub.send_all_on_topic('sched-created', sched.id)
        except UnknownError as unknown:
            raise unknown
        except Exception as e:
            raise e
        except Exception as e:
            raise UnknownError('_save_sched()')
        
    def open_details_handler(self, topic, data: SchedDTO):
        self.view.icon = data.icon
        self.view.name = data.name
        self.view.date = data.date
        self.view.duration = data.duration
        self.view.time = data.time
        self.view.priority = data.priority
        self.view.annotation = data.annotation

        action = None
        if topic == 'task-completed': action = 'edit'
        if topic == 'task-selected': action = 'back_taskcreator'
        if topic == 'task-display': action = 'back_scheduler'
        

        self.view.update_view()
        self.view.back_action(action)
        self.page.pubsub.send_all_on_topic('load-priorities', 'DetailsController')

        def clear(e):
            self.page.overlay.clear()
            self.page.update()
            pass

        self.page.overlay.append(
            ft.Stack(
                alignment= ft.alignment.center,
                
                controls= [
                    ft.Container(
                        width= self.page.window.width,
                        height= self.page.window.height,
                        bgcolor = '#0d000000',
                        on_click= clear,
                    ),

                    self.view,
                ]
            )
        )
        self.page.update()
        pass
    
    def __get_day(self, date):
        try:
            day = self.dayService.create(date= date)
        except IntegrityError:
            SESSION.rollback()
            day = self.dayService.find(date= date)
        except Exception as e: 
            raise UnknownError('__get_day()')
        return day

    def __get_priority(self, data):
        try:
            name = data['name']
            color = data['color']

            priority = self.priorityService.find(name= name)

            if priority is None: 
                return self.priorityService.create(
                    name= name,
                    color= color,
                    icon_id= 7,
                )
            if priority.color != color: 
                self.priorityService.update(priority.id, color)

            return priority
        except Exception:
            raise UnknownError('__get_priority()')

    def __get_task(self, name, duration, icon_src):
        icon = self.iconService.find(src= icon_src)
        try:
            return self.taskService.create(name= name, duration= duration, icon= icon)
        except IntegrityError as e:
            SESSION.rollback()
            task = self.taskService.find(name= name, duration= duration)
            if task.icon != icon: self.taskService.update(task.id, icon)
            return task
        except Exception:
            raise UnknownError('__get_task')
        
    def __get_sched(self, day, priority, task, hour, begin, annotation):
        try:
            return self.schedulerService.create(
                day= day,
                priority= priority,
                task= task,
                hour= hour,
                begin= begin,
                annotation= annotation,
            )
        except IntegrityError:
            SESSION.rollback()
            sched = self.schedulerService.find(day= day, task= task, hour=hour)
            
            if priority != sched.priority or annotation != sched.annotation:
                self.schedulerService.update(priority= priority, annotation= annotation, id=sched.id)
            return sched
        except NoFreeTime:
            print(f'*** error -> NoFreeTime: to implement ***') # when there's no available time in an hour...
        except TaskConflicted:
            print(f'*** error -> TaskConflicted: to implement ***') # when there is available time, but there is other tasks within period...
        except Exception:
            raise UnknownError('__get_sched()')