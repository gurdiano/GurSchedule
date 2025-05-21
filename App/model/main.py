from App.model.models import *
from App.model.config import *
from App.model.exc.CreateBaseException import CreateBaseException

from App.model.seeds import base

try:
    try:
        create_tables()
    except Exception as e:
        raise Exception('Error in create tables.')

    try:
        session = next(get_db())
    except Exception as e:
        raise CreateBaseException()
    
    try:
        item = session.query(Priority).first()
        if item is None: base.exec(session)
    except Exception as e:
        raise Exception('failed in base seeding.')

except Exception as e:
    print(f'error: {e}')
    drop_tables()

from App.model.services.SchedulerService import SchedulerService
from App.model.services.DayService import DayService
from App.model.services.IconService import IconService
from App.model.services.PriorityService import PriorityService
from App.model.services.TaskService import TaskService
import datetime

dayService = DayService(session)
iconService = IconService(session)
priorityService = PriorityService(session)
taskService = TaskService(session)
schedService = SchedulerService(session)