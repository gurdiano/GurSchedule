from App.model.models import Scheduler, Task, Icon

from App.view.service import session

from App.model.services import SchedulerService
from App.model.services import DayService

scheduler = SchedulerService(session)
day = DayService(session)

class SchedService():

    @staticmethod
    def get_scheds(date, time):
        hh = time.hour
        dd = day.find(date=date)
        return scheduler.find(hour=hh, day=dd)