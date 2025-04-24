from App.model.models import Scheduler
from sqlalchemy.exc import IntegrityError, StatementError
from App.model.services.__HourService import HourService
from App.model.exc.IntegrityError import IntegrityError as _IntegrityError


class SchedulerService():
    def __init__(self, session):
        self.session = session

    def create(self, hour, begin, day, priority, task, annotation=None):
        try:
            HourService.can_create(
                hour=hour,
                begin=begin,
                day=day,
                task=task
            )

            sess = self.session
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
        except IntegrityError:
            raise _IntegrityError(None, f'IntegrityError: the scheduling already exists!')
        except StatementError:
            raise Exception(f'StatementError: invalid input')
        except Exception as e:
            raise Exception(f'error: {type(e).__name__} failed to create scheduling! \nmsg:{e}')
        
    def find(self, id=None, hour=None, day=None, task=None):
        try:
            sess = self.session
            if id:
                return sess.query(Scheduler).filter_by(id=id).first()
            if hour and day and task:
                return sess.query(Scheduler).filter_by(hour=hour, day_id=day.id, task_id=task.id).first()
            if hour and day:
                return sess.query(Scheduler).filter_by(hour=hour, day_id=day.id).all()
        except Exception as e:
            raise Exception(f'error: {type(e).__name__} Could not read the schedule. Please enter the ID or the hour, day, and task to proceed.')
        
    def update(self, id, annotation=None, priority=None):
        try:
            sess = self.session
            obj = self.find(id=id)
            
            if annotation: obj.annotation = annotation
            if priority: obj.priority_id = priority.id

            sess.commit()
        except Exception as e:
            raise Exception(f'error: {type(e).__name__} failed to update scheduling!')
        
    def delete(self, id):
        try:
            sess = self.session
            obj = self.find(id=id)
            sess.delete(obj)
            sess.commit()
        except Exception as e:
            raise Exception(f'error: {type(e).__name__} failed to delete scheduling!')