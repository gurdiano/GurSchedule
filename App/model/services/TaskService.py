from App.model.models import Task
from sqlalchemy.exc import IntegrityError, StatementError

class TaskService():
    def __init__(self, session):
        self.session = session

    def create(self, name, duration, icon):
        try:
            sess = self.session
            obj = Task()

            obj.name = name 
            obj.duration = duration
            obj.icon_id = icon.id

            sess.add(obj)
            sess.commit()
            sess.refresh(obj)
            return obj
        except IntegrityError:
            raise Exception(f'IntegrityError: the {name} {duration} already exists!')
        except StatementError:
            raise Exception(f'StatementError: invalid input')
        except Exception as e:
            raise Exception(f'error: {type(e).__name__} failed to create task!')
        
    def find(self, id=None, name=None, duration=None):
        try:
            sess = self.session
            if id:
                return sess.query(Task).filter_by(id=id).first()
            if name and duration:
                return sess.query(Task).filter_by(name=name, duration=duration).first()
            if name and not duration:
                return sess.query(Task).filter_by(name=name).first()
        except Exception as e:
            raise Exception(f'error: {type(e).__name__} failed to read task!')
        
    def update(self, id, icon):
        try:
            sess = self.session
            obj = self.find(id=id)
            obj.icon_id = icon.id
            sess.commit()
        except Exception as e:
            raise Exception(f'error: {type(e).__name__} failed to update task!')