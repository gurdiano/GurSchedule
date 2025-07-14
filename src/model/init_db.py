from model.models import *
from model.config import *
from model.exc.CreateBaseException import CreateBaseException
from model.seeds import base

def initialize_database():
    try:
        create_tables()
    except Exception as e:
        raise Exception('Error in create tables.')

    try:
        with get_db() as session:
            item = session.query(Priority).first()
            if item is None: 
                base.exec(session)
    except Exception as e:
        raise CreateBaseException()
    

