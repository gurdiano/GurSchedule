from sqlalchemy import Column, Integer, String, Date, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import traceback
import datetime

from App.BackEnd.Entities import models
from App.BackEnd.Services import exceptions as person

class Day:
    def __init__(self, session):
        self.session = session
        pass
    
    def _find(self, id):
        if self.session.query(models.Day).filter_by(date=id).first() is not None:
            return True
        return False
    
    def create(self, date):
        if self._find(date): raise person.CreateException(date)
        day = models.Day(date=date)
        self.session.add(day)
        self.session.commit()

        return day
    
    def find_id(self, id):
        obj = self.session.query(models.Day).filter_by(date=id).first()
        if obj is None: raise person.ResourceNotFound(id)
        
        return obj
    
    def find_all(self):
        return self.session.query(models.Day).all()    

    def delete(self, id):
        obj = self.find_id(id)
        self.session.delete(obj)
        self.session.commit()        
        return None

class Hour:
    def __init__(self, session):
        self.session = session
        pass

    def _find(self, id):
        if self.session.query(models.Hour).filter_by(id=id).first() is not None:
            return True
        return False
    
    def create(self, number):
        if number >= 0 and number <= 23:
            hour = models.Hour(hour=number)
            return hour
        else:
            raise person.CreateException(number)
        
    def find_id(self, id):
        obj = self.session.query(models.Hour).filter_by(id=id).first()
        if obj is None: raise person.ResourceNotFound(id)

        return obj
    
    def find_all(self):
        return self.session.query(models.Hour).all()
    
class Work:
    def __init__(self, session):
        self.session = session

    def _find(self, name, duration):
        if self.session.query(models.Work).filter_by(name=name, duration=duration).first() is not None:
            return True
        return False
    
    def _find_name_dur(self, name, duration):
        obj = self.session.query(models.Work).filter_by(name=name, duration=duration).first()
        if obj is None: raise person.ResourceNotFound(name)
        return obj

    def create(self, name, duration=None, annotation=None, priority=None, icon=None):
        if self._find(name, duration): raise person.CreateException(name)

        work = models.Work(
            name=name,
            duration=duration,
            annotation=annotation,
            priority=priority,
            icon=icon,
        ) 

        self.session.add(work)
        self.session.commit()
        return work
    
    def find_id(self, id):
        obj = self.session.query(models.Work).filter_by(id=id).first()
        if obj is None: raise person.ResourceNotFound(id)
        return obj
    
    def find_all(self):
        return self.session.query(models.Work).all()    
    
    def update(self, id, duration=None, priority=None, annotation=None, icon=None):
        obj = self.find_id(id)
        
        if duration is not None:
            obj.duration = duration
        if annotation is not None:
            obj.annotation = annotation
        if priority is not None:
            obj.priority = priority
        if icon is not None:
            obj.icon = icon

        self.session.commit()
        return obj

    def delete(self, id):
        obj = self.find_id(id)
        self.session.delete(obj)
        self.session.commit()
        return None

class Task:
    def __init__(self, session):
        self.session = session

    def create(self, time):
        return models.Task(beginning=time)

    def find_id(self, id):
        obj = self.session.query(models.Task).filter_by(id=id).first()
        if obj is None: raise person.ResourceNotFound(id)
        return obj
    
    def find_all(self):
        return self.session.query(models.Task).all()    
    
    def update(self, id, work=None, hour=None, beginning=None):
        obj = self.find_id(id)
        
        if work is not None:
            obj.work = work
        if hour is not None:
            obj.hour = hour
        if beginning is not None:
            obj.beginning = beginning
  
        self.session.commit()
        return obj

    def delete(self, id):
        obj = self.find_id(id)
        self.session.delete(obj)
        self.session.commit()
        return None
    
    def _len(self, min, duration):
        if min is None: min = 0
        if duration is None: duration = 0

        seconds = 60
        hour = 60 * seconds 
        begin = min * seconds
        end = begin + duration
        _dur = hour - begin
        next = 0

        if end > hour:
            next = end - hour

        return  {
            'begin' : begin,
            'end' : end,
            'next' : next,
            'duration' : _dur
        }

    def has_conflict(self, task, duration, begin):
        work_dur = duration
        task_min = 0
        task_dur = 0

        if task is not None:
            task_min = task.beginning.minute
            task_dur = task.work.duration
    
        work_len = self._len(min=begin, duration=work_dur)
        task_len = self._len(min=task_min, duration=task_dur)

        work_begin = work_len['begin']
        work_end = work_len['end']
        work_next = work_len['next']

        task_begin = task_len['begin']
        task_end = task_len['end']

        if task_dur > 0:
            if work_begin >= task_begin and work_begin < task_end: return {'conflict' : True, 'type' : 'b-in', 'task': task, 'next': work_next} 
            if work_end > task_begin and work_end <= task_end: return {'conflict' : True, 'type' : 'e-in', 'task': task, 'next': work_next}
            if work_begin <= task_begin and work_end >= task_end: return {'conflict' : True, 'type' : 'bae-out',  'task': task, 'next': work_next}

        return {'conflict' : False, 'task': task, 'next': work_next}

def create_work(_work_service, work_name, duration, annotation, priority, icon):
    if _work_service._find(name=work_name, duration=duration):
        return _work_service._find_name_dur(name=work_name, duration=duration)
    else:  
        return _work_service.create(
            name=work_name, 
            duration=duration, 
            annotation=annotation, 
            priority=priority, 
            icon=icon,
        )
              
def create_day(_day_service, date):
    if _day_service._find(date):
        return _day_service.find_id(date)    
    else: 
        return _day_service.create(date)

def create_hour(session, _hour_service, hour_value, day):
    try:
        hour = session.query(models.Hour).filter_by(hour=hour_value, day_id=day.date).first()

        if hour is None:
            hour = _hour_service.create(hour_value)
            hour.day = day
            session.add(hour)
            session.commit()
            return hour
        else:
            return hour
    except person.CreateException as ex:
        raise person.ExceedsOneDay(hour_value)

def create_task(session, date=None, hour_value=None, minute_value=None, work_name=None, duration=None, annotation=None, priority=None, icon=None):
    day_service = Day(session)
    hour_service = Hour(session)
    work_service = Work(session)
    task_service = Task(session)

    try:
        def search_conflicts(duration, list, hour_value, minute, day):
            two = []
            dur = 0
            next = 0
            _minute = minute
            _hour = hour_value
            
            hour = session.query(models.Hour).filter_by(hour=_hour, day=day).first()
       
            if hour is not None and hour.tasks:
                for tk in hour.tasks:
                    search = task_service.has_conflict(
                        task=tk,
                        begin=_minute,
                        duration=duration
                    )
                    two.append(search)

                list.append(two)
            else:
                search = task_service.has_conflict(
                    task=None,
                    begin=_minute,
                    duration=duration
                )
                two.append(search)
                list.append(two)

            for search in two:
                if search['next'] != 0:
                    dur = search['next']
                    next = _hour + 1
                    _minute = 0
                    break
                
            if dur > 0:
                search_conflicts(dur, list, next, _minute, day)
            return list
        def recursion_verify(conflicts, _search, _hour):
            next = []
            plus = 0 
        
            for sublist in _search:
                for _task in sublist:
                    if _task['conflict'] == True:
                        conflicts.append(_task)
                    if _task['next'] != 0 and _task['next'] not in next:
                        next.append(_task['next'])

            if conflicts:
                raise person.ConflictingTasks(conflicts)

            if next:
                for dur in next:
                    plus += 1
                    balance = 3600 if dur > 3600 else dur

                    create_task(
                        session= session,
                        date = date,
                        hour_value= _hour + plus,
                        minute_value= 0,
                        work_name= work_name,
                        duration= balance,
                        annotation= annotation,
                        priority= priority,
                        icon= icon,
                    )
        def get_real_duration(min, duration):
            r_duration = task_service._len(
                min= minute_value,
                duration= duration
            )
            available = r_duration['duration']
            return available if duration > available else duration

        beginning = datetime.time(hour_value if hour_value <= 23 else 1, minute_value)            
        day = create_day(day_service, date); print(f'The day was accessed... {day}')
        r_dur = get_real_duration(
            min=minute_value,
            duration=duration
        )
        hour = create_hour(
            _hour_service= hour_service,
            hour_value= hour_value,
            day= day,
            session= session
        ); print(f'The hour was accessed {hour}h')
        work = create_work(
            _work_service= work_service,
            work_name= work_name,
            duration= r_dur,
            annotation= annotation,
            priority= priority,
            icon= icon
        ); print(f'The work was accessed {work}')
        search = search_conflicts (
            hour_value= hour_value, 
            minute= minute_value, 
            duration= duration, 
            list= [], 
            day= day
        )

        conflicts = []
        recursion_verify(conflicts, search, hour_value)

        task = task_service.create(time=beginning)
        task.hour = hour
        task.work = work

        session.add(task)
        print(f'The task was created {task}')

    except person.CreateException as err:
        print(f"task error: {err}")
        print(f"Invalid input hour: {hour_value}h")
        print(f"Invalid input date: {date}")
        print(f"Invalid input work name: {work_name}")

    except person.ResourceNotFound as err:
        print(f"task error: {err}")
        print(f"Invalid input hour: {hour_value}h")
        print(f"Invalid input date: {date}")
        print(f"Invalid input work name: {work_name}")
    
    except person.ExceedsOneDay as err:
        print(f'task error: {err}')

    except person.ConflictingTasks as err:
        print(f"task error: items are in conflict")

        want_adjust(session,
            tasks=conflicts,
            beginning=beginning, 
            duration=duration
        )

        create_task(
            session = session,
            date= date, 
            hour_value= hour_value, 
            minute_value= minute_value, 
            work_name= work_name, 
            duration= duration, 
            annotation= annotation, 
            priority= priority, 
            icon= icon
        )
    
    except Exception as err:
        print(f"unknown error: {err}")
        traceback.print_exc()
 
def want_adjust(session, tasks=None, beginning=None, duration=None):
    print()
    print()
    try:
        def __get_work(_work_service, old_obj, new_duration):
            __name=old_obj.name,
            __duration=new_duration,
            __annotation=old_obj.annotation,
            __priority=old_obj.priority,
            __icon=old_obj.icon,

            if _work_service._find(name=__name, duration=__duration):
                return _work_service._find_name_dur(name=__name, duration=__duration)
            else:
                return _work_service.create(
                    name=__name,
                    duration=__duration,
                    annotation=__annotation,
                    priority=__priority,
                    icon=__icon
                )          
        def __fix(_task_service, _task, _work, minute):
            _task_id = _task.id
            _hour = _task.beginning
            _old_dur = _task.work.duration
            _beginning = datetime.time(_hour.hour, minute)

            _task_service.update(
                id = _task_id,
                work = _work,
                beginning=_beginning
            )

            print(f'The duration has been adjusted from {_old_dur} to {_task.work.duration}')
            print(f'The beginning has been delayed from {_hour} to {_beginning}') 
            print()
        def __task(_task, type, _task_service, task_old, task_now):
            _work_service = Work(session)
            __MIN = 60

            _now_begin = task_now['begin']
            _now_end = task_now['end']
            _old_begin = task_old['begin']
            _old_end = task_old['end']
            _old_dur = _task.work.duration

            if type == 'bae-out': 
                _task_service.delete(_task.id)
                print(f'The task({_task.work.name}) was removed...')

            if type == 'b-in':
                adjust = _old_end - _now_begin
                dur = _old_dur - adjust
                _work = __get_work(_work_service, task.work, dur)

                __fix(_task_service, _task, _work, _task.beginning.minute)

            if type == 'e-in': 
                adjust  = _now_end - _old_begin
                min_old = _task.beginning.minute
                min_add = int(adjust / __MIN) + min_old
                dur = _old_dur - adjust
                _work = __get_work(_work_service, task.work, dur)

                __fix(_task_service, _task, _work, min_add)

        task_service = Task(session)

        task_now = task_service._len(
            min=beginning.minute, 
            duration=duration
        )

        for dict in tasks:
            task = dict['task']
            type = dict['type']

            _task_old = task_service._len(
                min=task.beginning.minute, 
                duration=task.work.duration
            )

            __task(task, type, task_service, _task_old, task_now)
    except Exception as err:
        print(f'want adjust error: {err}')
        traceback.print_exc()

def create_icon(session, name=None, src=None, priority=None):

    obj = models.Icon(
        name = name,
        src = src,
        priority = priority
    )

    session.add(obj)
    session.commit()

def find_icon(session, id=None):
    return session.query(models.Icon).filter_by(id=id).first()

def fetch_task(session, hour:Integer=None, day:Date=None):
    if session.query(models.Day).filter_by(date=day).first(): return None

    session.query(models.Hour).filter_by(date=day).first()
    

    

    return 