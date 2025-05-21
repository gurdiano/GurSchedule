from App.model.services import SchedulerService
from App.model.services import PriorityService

from App.dtos.SchedDTO import SchedDTO
from App.dtos.RowDTO import RowDTO
from App.dtos.DisplayDTO import DisplayDTO

from App.model.exc.UnknownError import UnknownError

class PiruError(Exception):
    def __init__(self, *args, msgg):
        super().__init__(*args)

        self.msgg = msgg

from .. import SESSION

from .__CreatorController import CreatorController
from .__DetailsController import DetailsController
from .__DisplayController import DisplayController

class TaskController:
    def __init__(self, page):
        self.page = page    
        self.details = None
        self.last_call = None

        self.schedulerService = SchedulerService(SESSION)
        self.priorityService = PriorityService(SESSION)

        self.creatorController = CreatorController(page)
        self.detailsController = DetailsController(page)
        self.displayController = DisplayController(page)
        
        self.page.pubsub.subscribe_topic('task-display', self.task_display_handler)
        self.page.pubsub.subscribe_topic('row-onclick', self.row_on_click_handler)
        self.page.pubsub.subscribe_topic('task-completed', self.task_completed_handler)
        self.page.pubsub.subscribe_topic('task-selected', self.task_selected_handler)
        self.page.pubsub.subscribe_topic('load-priorities', self.load_priorities_handler)
        self.page.pubsub.subscribe_topic('last-call', self.last_call_handler)
        self.page.pubsub.subscribe_topic('sched-load', self.sched_load_handler)
        self.page.pubsub.subscribe_topic('sched-created', self.sched_created_handler)

        self.page.pubsub.subscribe_topic('priority-created', self.priority_created_handler)

    def sched_load_handler(self, topic, message: DisplayDTO):
            self.displayController.created_sched_handler(control= message.parent, sched_id= message.sched_id)
            message.parent.update()

    def sched_created_handler(self, topic, sched_id):
        control = self.last_call.control
        self.displayController.created_sched_handler(control= control, sched_id= sched_id)

        control.update()
        self.page.overlay.clear()
        self.page.update()
        pass

    def task_selected_handler(self, topic, message: SchedDTO):
        self.page.overlay.clear()
        self.page.update()
        self.detailsController.open_details_handler(topic, message)
        pass

    def task_completed_handler(self, topic, message: SchedDTO):
        self.page.overlay.clear()
        self.page.update()
        self.detailsController.open_details_handler(topic, message)
        pass
    
    def task_display_handler(self, topic, message: DisplayDTO):
        sched = self.schedulerService.find(id= message.sched_id)
        parent  = message.parent

        schedDTO = self.__schedDTO(sched)

        rowDTO = RowDTO(
            n_row= parent.data['row'],
            n_column= parent.data['column'],
            date= parent.data['date'],
            time= parent.data['time'],
            control= parent.control
        )

        self.last_call = rowDTO
        self.detailsController.open_details_handler(topic, schedDTO)
        pass

    def last_call_handler(self, topic, message: RowDTO):
        self.last_call = message

    def row_on_click_handler(self, topic, message: RowDTO):
        last_call = self.last_call
        message = message if message else self.last_call
        self.creatorController.open_creator_handler(last_call, message)
        pass

    def priority_created_handler(self, topic, message):
        #building...
        priorities = self.__load_priorities()
        self.creatorController.update_priorities_handler(priorities)
        pass

    def load_priorities_handler(self, topic, message):
        priorities = self.__load_priorities()

        if message == 'CreatorController':
            self.creatorController.get_priorities_handler(priorities)
        if message == 'DetailsController':
            self.detailsController.get_priorities_handler(priorities)

        pass

    def __load_priorities(self):
        priorities = self.priorityService.get_last_items()
        main_priorities = [
            self.priorityService.find(id= 9),
            self.priorityService.find(id= 1),
            self.priorityService.find(id= 4),
            self.priorityService.find(id= 3),
            self.priorityService.find(id= 8),
        ]
        other_priorities = [item for item in priorities if item not in main_priorities]
        main_priorities.extend(other_priorities)

        all_priorities = []
        for priority in main_priorities:
            res = {
                'name': priority.name,
                'src': priority.icon.src,
                'color': priority.color,
            }
            all_priorities.append(res)
        return all_priorities

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