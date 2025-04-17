from App.model.models import Priority
from sqlalchemy.exc import IntegrityError

class PriorityService():
    def __init__(self, session):
        self.session = session

    def create(self, name, color, icon):
        try:
            sess = self.session
            obj = Priority()

            obj.name = name
            obj.color = color
            obj.icon_id = icon.id

            sess.add(obj)
            sess.commit()
            sess.refresh(obj)
            return obj
        except IntegrityError:
            raise Exception(f'IntegrityError: the {name} already exists!')
        except Exception as e:
            raise Exception(f'error: {type(e).__name__} failed to create a Priority!')

    def find(self, id=None, name=None, color=None):
        try:
            sess = self.session
            if id:
                return sess.query(Priority).filter_by(id=id).first()
            if name:
                return sess.query(Priority).filter_by(name=name).first()
            if color:
                return sess.query(Priority).filter_by(color=color).first()
        except Exception as e:
            raise Exception(f'error: {type(e).__name__} failed to read a Priority!')
        
    def update(self, id, color):
        try:
            sess = self.session
            obj = self.find(id=id)
            obj.color = color
            sess.commit()
        except Exception as e:
            raise Exception(f'error: {type(e).__name__} failed to update priority!')
