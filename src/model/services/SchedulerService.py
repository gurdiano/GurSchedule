from model.models import Scheduler
from model.services.__HourService import HourService

from sqlalchemy.exc import IntegrityError, StatementError

from model.exc.IntegrityError import IntegrityError as _IntegrityError
from model.exc.NoFreeTime import NoFreeTime
from model.exc.TaskConflicted import TaskConflicted

class SchedulerService():
    def __init__(self, session):
        self.session = session

    def create(self, hour, begin, day, priority, task, annotation=None):
        try:
            if self.find(day= day, hour= hour, task=task): 
                raise _IntegrityError(None, f'IntegrityError: the scheduling already exists!')
            
            sess = self.session

            HourService.can_create(session=sess, hour=hour, begin=begin, day=day, task=task)

            obj = Scheduler()
            obj.hour = hour
            obj.begin = begin
            obj.annotation = annotation
            obj.day_id = day.id
            obj.priority_id = priority.id
            obj.task_id = task.id

            sess.add(obj)
            sess.commit()
            sess.refresh(obj)
            return obj
        except NoFreeTime as personException:
            raise personException
        except TaskConflicted as personException:
            raise personException
        except _IntegrityError as personException:
            raise personException
        except IntegrityError:
            raise _IntegrityError(None, f'IntegrityError: the scheduling already exists!')
        except StatementError:
            raise Exception(f'StatementError: invalid input')
        except Exception as e:
            raise Exception(f'SchedulerService.create() failed to create scheduling! msg:{e}')
        
    def find(self, id=None, hour=None, day=None, task=None):
        try:
            sess = self.session
            if id:
                return sess.query(Scheduler).filter_by(id=id).first()
            if hour and day and task:
                return sess.query(Scheduler).filter_by(hour=hour, day_id=day.id, task_id=task.id).first()
            if hour and day:
                return sess.query(Scheduler).filter_by(hour=hour, day_id=day.id).first()
        except Exception as e:
            raise Exception(f'error: {type(e).__name__} Could not read the schedule. Please enter the ID or the hour, day, and task to proceed.')
        
    def find_all(self, hour=None, day=None):
        try:
            sess = self.session
            if day and hour:
                return sess.query(Scheduler).filter_by(hour=hour, day_id=day.id).all()
            if day:
                return sess.query(Scheduler).filter_by(day_id = day.id).all()
        except Exception as e:
            raise Exception(f'error: {type(e).__name__} Could not find all schedules.')

    def update(self, id, annotation=None, priority=None):
        try:
            sess = self.session
            obj = self.find(id=id)
            
            if annotation: obj.annotation = annotation
            if priority: obj.priority_id = priority.id

            sess.commit()
            sess.refresh(obj)
        except Exception as e:
            raise Exception(f'error: {type(e).__name__} failed to update scheduling!')
        
    def delete(self, id):
        try:
            sess = self.session
            obj = self.find(id=id)

            if obj:
                sess.delete(obj)
                sess.commit()
        except Exception as e:
            raise Exception(f'error: {type(e).__name__} failed to delete scheduling!')

    def get_last_items(self, n_items, id=None):
        try:
            sess = self.session
            if id: return sess.query(Scheduler).filter(Scheduler.id < id).order_by(Scheduler.id.desc()).limit(n_items).all()

            return sess.query(Scheduler).order_by(Scheduler.id.desc()).limit(n_items).all()
        except Exception as e:
            raise Exception(f'{type(e).__name__} Could not get_last_items.')

    def get_distinct_last_items(self, n_items, id=None, distinct=None, keys=None, remain= None):
        if distinct is None: distinct = []
        if keys is None: keys = set()
        if remain is None: remain = n_items

        if len(distinct) == n_items: return distinct
        items = self.get_last_items(remain, id)
        if items == []: return distinct

        for item in items:
            task = item.task.id
            if task not in keys:
                keys.add(task)
                distinct.append(item)

        last_item = items[-1].id
        remain = n_items - len(distinct)

        return self.get_distinct_last_items(n_items, last_item, distinct, keys, remain)