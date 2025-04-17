from App.model.models import Day
from sqlalchemy.exc import IntegrityError, StatementError

class DayService():
    def __init__(self, session):
        self.session = session

    def create(self, date):
        try:
            sess = self.session
            obj = Day(date=date)

            sess.add(obj)
            sess.commit()
            sess.refresh(obj)

            return obj
        except IntegrityError:
            raise Exception(f'IntegrityError: the date {date} already exists!')
        except StatementError:
            raise Exception(f'StatementError: input ({date}) must be a date!')
        except Exception as e:
            raise Exception(f'failed to create a day! error: {type(e).__name__}')
        
    def find(self, id=None, date=None):
        try:
            sess = self.session
            if id:
                return sess.query(Day).filter_by(id=id).first()
            if date:
                return sess.query(Day).filter_by(date=date).first()
        except Exception as e:
            raise Exception(f'failed to read a day! error: {id}{date} ,{type(e).__name__}')
