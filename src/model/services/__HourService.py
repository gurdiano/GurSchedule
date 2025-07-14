from model.exc.TaskConflicted import TaskConflicted
from model.exc.NoFreeTime import NoFreeTime

from model.models import Day

from datetime import datetime, date, timedelta

class HourService():
    @staticmethod
    def can_create(session, day, hour, begin, task):
        day = session.query(Day).filter_by(id = day.id).first()

        scheds =  day.schedulers
        duration = task.duration

        matchs = HourService._get_matchs(scheds, hour)
        tasks = HourService._get_tasks(matchs)

        is_free_time = HourService.is_free_time(tasks, duration)
        is_conflicted = HourService.is_conflicted(matchs, begin, duration)

        if is_conflicted: 
            raise TaskConflicted(is_conflicted, 'There is a conflict with one of the existing tasks.')
        
        if not is_free_time: raise NoFreeTime(is_conflicted, 'No time available to create this task.')

        return True

    @staticmethod
    def is_free_time(tasks, duration):
        busy = HourService._get_busytime(tasks)
        hour = 60 #minutes
        return False if busy + duration > hour else True

    @staticmethod
    def is_conflicted(matchs, begin, duration):
        temp_date = date(2025, 4, 14)
        begin_time = datetime.combine(temp_date, begin) 
        end_time = begin_time + timedelta(minutes=duration)

        conflicted = []
        for sched in matchs:
            task_begin = datetime.combine(temp_date, sched.begin)
            task_duration = sched.task.duration
            task_end = task_begin + timedelta(minutes=task_duration)
            if begin_time < task_end and task_begin < end_time: conflicted.append(sched)

        return conflicted

    @staticmethod
    def _get_matchs(scheds, hour):
        matchs = []
        for sched in scheds:
            if sched.hour == hour: matchs.append(sched)
        return matchs
    
    @staticmethod
    def _get_tasks(matchs):
        tasks = []
        for sched in matchs:
            task = sched.task
            tasks.append(task)
        return tasks
    
    @staticmethod
    def _get_busytime(tasks):
        time = 0 
        for task in tasks:
            duration = task.duration
            time += duration 
        return time