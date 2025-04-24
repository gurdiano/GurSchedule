from App.model.models import Icon
from sqlalchemy.exc import IntegrityError, StatementError
from App.model.exc.IntegrityError import IntegrityError as _IntegrityError

class IconService():
    def __init__(self, session):
        self.session = session

    def create(self, src):
        try:
            sess = self.session
            obj = Icon(src=src)
            sess.add(obj)
            sess.commit()
            sess.refresh(obj)
            return obj
        except IntegrityError:
            raise _IntegrityError(src, f'IntegrityError: the {src} already exists!')
        except StatementError:
            raise Exception(f'StatementError: input ({src}) must be a path!')
        except Exception as e:
            raise Exception(f'error: {type(e).__name__} failed to create icon!')
        
    def find(self, id=None, src=None):
        try:
            sess= self.session 
            if id:
                return sess.query(Icon).filter_by(id=id).first()
            if src:
                return sess.query(Icon).filter_by(src=src).first()
        except Exception as e:
            raise Exception(f'error: {type(e).__name__} failed to read icon!')