from App.model.models import *
from App.model.config import *
from App.model.seeds.base import create_base
from App.model.exc.CreateBaseException import CreateBaseException

from App.model.seeds.test01 import create_test01

try:
    try:
        create_tables()
    except Exception as e:
        raise Exception('Error in create tables.')

    try:
        session = next(get_db())
        create_base(session)
    except Exception as e:
        raise CreateBaseException()

    try:
        create_base(session)
    except Exception:
        raise Exception('failed in created base.')

    try:
        create_test01(session)
    except Exception:
        raise Exception('failed in popolar base.')
    
except Exception as e:
    print(f'error: {e}')
    drop_tables()


from App.model.services.SchedulerService import SchedulerService
from App.model.services.DayService import DayService
from App.model.services.IconService import IconService
from App.model.services.PriorityService import PriorityService
from App.model.services.TaskService import TaskService
from datetime import date, time

dayService = DayService(session)
iconService = IconService(session)
priorityService = PriorityService(session)
taskService = TaskService(session)
schedService = SchedulerService(session)

sched = schedService.find(id=9)
sched.priority_id = 9
session.commit()

dd1 = dayService.create(date=date(2025, 4, 6))
dd2 = dayService.create(date=date(2025, 4, 7))
dd3 = dayService.create(date=date(2025, 4, 8))
dd4 = dayService.create(date=date(2025, 4, 9))
dd5 = dayService.create(date=date(2025, 4, 10))
dd6 = dayService.create(date=date(2025, 4, 11))
dd7 = dayService.create(date=date(2025, 4, 12))

pp1 = priorityService.find(id=1)
pp2 = priorityService.find(id=2)
pp3 = priorityService.find(id=3)
pp4 = priorityService.find(id=4)
pp5 = priorityService.find(id=9)

tt1 = taskService.find(id=1)
tt2 = taskService.find(id=2)
tt3= taskService.find(id=3)
tt4 = taskService.find(id=4)
tt5 = taskService.find(id=5)
tt6 = taskService.find(id=6)
tt7 = taskService.find(id=7)

ss1 = schedService.create(day=dd1, begin=time(10, 0), priority=pp1, task=tt1, hour=10)
ss2 = schedService.create(day=dd2, begin=time(11, 0), priority=pp2, task=tt2, hour=11)
ss3 = schedService.create(day=dd3, begin=time(12, 0), priority=pp3, task=tt3, hour=12)
ss4 = schedService.create(day=dd4, begin=time(13, 0), priority=pp4, task=tt4, hour=13)
ss5 = schedService.create(day=dd5, begin=time(14, 0), priority=pp5, task=tt5, hour=14)
ss6 = schedService.create(day=dd6, begin=time(15, 0), priority=pp1, task=tt6, hour=15)
ss7 = schedService.create(day=dd7, begin=time(16, 0), priority=pp2, task=tt7, hour=16)

session.add(ss1)
session.commit()
