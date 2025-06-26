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
from App.dtos.RowDTO import RowDTO

from App.model.config import get_db

class DetailsController:
    def __init__(self, page):
        self.page = page
        self.view = TaskDetails(self, page)

    def get_priorities_handler(self, priorities):
        self.view.set_options(priorities)
        self.view.dropdown.options = self.view.options
        self.view.dropdown.update()

    def on_back_action(self):
        self.page.overlay.clear()
        self.page.pubsub.send_all_on_topic('row-onclick', None)
        pass

    def on_remove_sched(self):
        with get_db() as session:
            schedulerService = SchedulerService(session)
            _id = self.view.data['id']
            schedulerService.delete(_id)

            self.page.pubsub.send_all_on_topic('sched-remove', None)
            pass

    def on_save_sched(self, data: SchedDTO):
        try:
            day = self.__get_day(data.date)
            priority = self.__get_priority(data.priority)
            task = self.__get_task(data.name, data.duration, data.icon)

            time = data.time
            hour = data.time.hour
            annotation = data.annotation
            
            sched = self.__get_sched(
                day= day,
                priority= priority,
                task= task,
                hour= hour,
                begin= time,
                annotation= annotation,
            )

            if sched: 
                rowDTO = RowDTO(date= data.date, time= sched.begin)

                self.view.open_creation_success('on_save_sched()')
                self.page.pubsub.send_all_on_topic('sched-created', rowDTO)
        except UnknownError as unknown:
            raise unknown
        except NoFreeTime:
            None
        except TaskConflicted:
            None
        except Exception as e:
            raise UnknownError('on_save_sched()')
        
    def on_edit_sched(self, data: SchedDTO):
        with get_db() as session:
            schedulerService = SchedulerService(session)

            old_id = self.view.data['id']
            old_sched = schedulerService.find(old_id)

            old_data = SchedDTO(
                name= old_sched.task.name,
                duration= old_sched.task.duration,
                date= old_sched.day.date,
                time= old_sched.begin,
                priority= {'name': old_sched.priority.name, 'color': old_sched.priority.color},
                icon= old_sched.task.icon.src,
                annotation= old_sched.annotation
            )

            schedulerService.delete(id= old_id)
            try:
                day = self.__get_day(data.date)
                priority = self.__get_priority(data.priority)
                task = self.__get_task(data.name, data.duration, data.icon)

                time = data.time
                hour = data.time.hour
                annotation = data.annotation
                
                sched = self.__get_sched(
                    day= day,
                    priority= priority,
                    task= task,
                    hour= hour,
                    begin= time,
                    annotation= annotation,
                )

                if sched: 
                    rowDTO = RowDTO(date= data.date, time= sched.begin)

                    self.view.open_creation_success('on_edit_sched()')
                    self.page.pubsub.send_all_on_topic('sched-edit', rowDTO)
                return
            except UnknownError as unknown:
                raise unknown
            except NoFreeTime:
                None
            except TaskConflicted:
                None
            except Exception as e:
                raise UnknownError('on_edit_sched()')
            
            try:
                day = self.__get_day(old_data.date)
                priority = self.__get_priority(old_data.priority)
                task = self.__get_task(old_data.name, old_data.duration, old_data.icon)

                time = old_data.time
                hour = old_data.time.hour
                annotation = old_data.annotation
                
                sched = self.__get_sched(
                    day= day,
                    priority= priority,
                    task= task,
                    hour= hour,
                    begin= time,
                    annotation= annotation,
                )
                self.view.data['id'] = sched.id
            except Exception as e:
                raise UnknownError('on_edit_sched() trying remake sched')
        pass

    def on_overwrite_sched(self, data: SchedDTO):
        with get_db() as session:
            schedulerService = SchedulerService(session)
        
            try:
                day = self.__get_day(data.date)
                priority = self.__get_priority(data.priority)
                task = self.__get_task(data.name, data.duration, data.icon)

                time = data.time
                annotation = data.annotation
                hour = time.hour

                if self.view.data: schedulerService.delete(id= self.view.data['id'])

                for sched_id in self.view.conflicts_id:
                    schedulerService.delete(id= sched_id)
                
                sched = self.__get_sched(
                    day= day,
                    priority= priority,
                    task= task,
                    hour= hour,
                    begin= time,
                    annotation= annotation,
                )

                if sched: self.view.open_creation_success('on_overwrite_sched()')

                self.page.pubsub.send_all_on_topic('sched-overwrite', None)
            except UnknownError as unknown:
                raise unknown
            except Exception as e:
                raise UnknownError('on_overwrite_sched()')

    def open_details_handler(self, topic, data: SchedDTO):
        self.view.icon = data.icon
        self.view.name = data.name
        self.view.date = data.date
        self.view.duration = data.duration
        self.view.time = data.time
        self.view.priority = data.priority
        self.view.annotation = data.annotation
        self.view.data = data.sched_id

        action = None
        if topic == 'task-completed': action = 'creator'
        if topic == 'task-selected': action = 'preview'
        if topic == 'task-display': action = 'edit'
        
        self.view.update_view()
        self.view.set_mode(action)
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
    
    def _on_load_all_icons(self):
        with get_db() as session:
            iconService = IconService(session)

            srcs = []
            icons = iconService.get_last_items()
            for icon in icons:
                srcs.append(icon.src)

            return srcs
        
    def __get_day(self, date):
        with get_db() as session:
            dayService = DayService(session)

            try:
                day = dayService.create(date= date)
            except IntegrityError:
                session.rollback()
                day = dayService.find(date= date)
            except Exception as e: 
                raise UnknownError('__get_day()')
            return day

    def __get_priority(self, data):
        with get_db() as session:
            priorityService = PriorityService(session)

            try:
                name = data['name']
                color = data['color']

                priority = priorityService.find(name= name)

                if priority is None: 
                    return priorityService.create(
                        name= name,
                        color= color,
                        icon_id= 7,
                    )
                if priority.color != color: 
                    priorityService.update(priority.id, color)

                return priority
            except Exception:
                raise UnknownError('__get_priority()')

    def __get_task(self, name, duration, icon_src):
        with get_db() as session:
            iconService = IconService(session)
            taskService = TaskService(session)

            icon = iconService.find(src= icon_src)
            try:
                return taskService.create(name= name, duration= duration, icon= icon)
            except IntegrityError as e:
                session.rollback()
                task = taskService.find(name= name, duration= duration)
                if task.icon != icon: taskService.update(task.id, icon)
                return task
            except Exception:
                raise UnknownError('__get_task')
        
    def __get_sched(self, day, priority, task, hour, begin, annotation):
        with get_db() as session:
            schedulerService = SchedulerService(session)

            try:
                return schedulerService.create(
                    day= day,
                    priority= priority,
                    task= task,
                    hour= hour,
                    begin= begin,
                    annotation= annotation,
                )
            except IntegrityError:
                session.rollback()
                sched = schedulerService.find(day= day, task= task, hour=hour)
                if priority != sched.priority or annotation != sched.annotation:
                    schedulerService.update(priority= priority, annotation= annotation, id=sched.id)
                return sched
            except NoFreeTime as personException:
                self.__open_overwrite_confirm(personException.scheds)
                raise personException
            except TaskConflicted as personException:
                self.__open_overwrite_confirm(personException.scheds)
                raise personException
            except Exception:
                raise UnknownError('__get_sched()')
            
    def __open_overwrite_confirm(self, scheds):
        schedsDTO = []
        conflicts_id = []
        for sched in scheds:
            schedsDTO.append(
                SchedDTO(
                    name= sched.task.name,
                    date= sched.day.date,
                    time= sched.begin,
                    duration= sched.task.duration,
                    sched_id= sched.id,
                )
            )
            conflicts_id.append(sched.id)
        
        self.view.conflicts_id = conflicts_id
        self.view.open_overwrite_confirm(schedsDTO)
        pass