from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

import Entities.models as models
import Services.services as service

import datetime
import threading, time
import traceback

# URL de conexão usando SQLAlchemy com o driver psycopg2
DATABASE_URL = "sqlite:///GurSchedule.db"
engine = create_engine(DATABASE_URL)

Base = models.Base

# Cria as tabelas no banco de dados
Base.metadata.create_all(engine)

# Cria uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()

import os

try:
    day_ser = service.Day(session)
    hour_ser = service.Hour(session)
    work_ser = service.Work(session)
    task_ser = service.Task(session)

    try:
        ##Teste
        d1 = models.Day(date=datetime.date(1999,12,12))
        d2 = models.Day(date=datetime.date(2002,3,12))
        d3 = models.Day(date=datetime.date(1999,11,30))
        
        h1 = models.Hour(hour=22)
        h2 = models.Hour(hour=8)
        h3 = models.Hour(hour=12)

        w1 = models.Work(name='Seila', duration=600)
        w2 = models.Work(name='Nada', duration=600)
        w3 = models.Work(name='Trabson', duration=600)

        h1.day = d1
        h2.day = d2
        h3.day = d3
        
        t1 = models.Task(beginning=datetime.time(14, 30))
        t1.hour = h1
        t1.work = w1

        t2 = models.Task(beginning=datetime.time(14, 30))
        t2.hour = h2
        t2.work = w2
        
        t3 = models.Task(beginning=datetime.time(14, 30))
        t3.hour = h3
        t3.work = w3

        session.add(d1)
        session.add(h1)
        session.add(w1)

        session.add(d2)
        session.add(h2)
        session.add(w2)

        session.add(d3)
        session.add(h3)
        session.add(w3)

        session.add(t1)
        session.add(t2)
        session.add(t3)
    except Exception as err:
        print(f'Error on seeding teste: {err}')

    try:
        def seeding ():
            hour = hour_ser.create(number=11)
            hour.day = d1
            session.add(hour)

            t1 = task_ser.create(datetime.time(hour.hour, 10))
            t2 = task_ser.create(datetime.time(hour.hour, 30))
            t3 = task_ser.create(datetime.time(hour.hour, 40))

            w1 = work_ser.create(name='Passear', duration=10*60)
            w2 = work_ser.create(name='Work', duration=10*60)
            w3 = work_ser.create(name='Estudar', duration=10*60)

            session.add(w1)
            session.add(w2)
            session.add(w3)
            
            t1.hour = hour
            t2.hour = hour
            t3.hour = hour

            t1.work = w1
            t2.work = w2
            t3.work = w3

            session.add(t1)
            session.add(t2)
            session.add(t3)
        seeding()
    except Exception as err:
        print(f'Error on seeding 1: {err}')

    try:
        def seeding2 ():
            hh1 = hour_ser.create(number=12)
            hh2 = hour_ser.create(number=13)
            hh3 = hour_ser.create(number=14)

            hh1.day = d1
            hh2.day = d1
            hh3.day = d1

            session.add(hh1)
            session.add(hh2)
            session.add(hh3)
        
            # ww = work_service.find_id(id='Work')

            # t4 = task_service.create(time = datetime.time(hh1.hour, 20))
            # t5 = task_service.create(time = datetime.time(hh2.hour, 20))
            # t6 = task_service.create(time = datetime.time(hh3.hour, 20))

            # t4.work = ww
            # t5.work = ww
            # t6.work = ww

            # t4.hour = hh1
            # t5.hour = hh2
            # t6.hour = hh3

            # session.add(t4)
            # session.add(t5)
            # session.add(t6)
        seeding2 () 

        service.create_task(session=session,
            date=datetime.date(1999, 12, 12),
            work_name='AOSKOASKOK',
            hour_value=23,
            minute_value=35,
            duration = (60 * 180)
        )

        session.commit()
        session.close()
    except Exception as err:
        print(f'Error on seeding 2: {err}')

except Exception as e:
    session.close()
    Base.metadata.drop_all(engine)
    # print(f"MAIN.PY ERROR>>>>> ::: {e}")
    print(f"MAIN.PY ERROR>>>>> ::: {e}")

try:
    con = True

    def fechar():
        global con
        input("Pressione Enter para parar...\n") 
        con = False

    thread = threading.Thread(target=fechar)
    thread.start()

    while con:
        time.sleep(1)

    thread.join()

    ahhh = Base.metadata.drop_all(engine)

except Exception as err:
    print('erro em apagar o banco...')