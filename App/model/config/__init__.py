from .base import Base
from .session import SessionLocal, engine

__all__ = ['Base' ,'SessionLocal', 'create_tables', 'drop_tables', 'get_db']

def create_tables():
    Base.metadata.create_all(bind=engine)

def drop_tables():
    Base.metadata.drop_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()