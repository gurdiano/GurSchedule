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
    except Exception as e:
        raise CreateBaseException()
    
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