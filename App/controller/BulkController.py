import datetime

from App.view.components.Bulk import Bulk
from App.view.resources.utility import convs

from App.model.config import get_db
from App.model.services import SchedulerService
from App.model.services import DayService
from App.model.exc.IntegrityError import IntegrityError
from App.model.exc.UnknownError import UnknownError

class BulkController:
    def __init__(self, page):
        self.page = page
        self.week = convs.initial_date_week(datetime.date.today())
        self.view = Bulk(self, page)

    def date_update_handler(self, topic, message):
        self.week = message
        self.view.date_week = message
        self.view.update_overlay()
        pass

    def copy_bulk_handler(self, topic, message):
        self.view.date_week = self.week
        self.view.open_copy_bulk()
        pass

    def on_bulk_active(self):
        self.page.pubsub.send_all_on_topic('bulk-activated', None)
        pass
    
    def on_back_week(self):
        date = convs.back_date_week(self.week)
        self.week = date
        self.page.pubsub.send_all_on_topic('picker-value', date)
        pass

    def on_next_week(self):
        date = convs.next_date_week(self.week)
        self.week = date
        self.page.pubsub.send_all_on_topic('picker-value', date)
        pass

    def on_copy_week_schedules(self):
        with get_db() as session:
            dayService = DayService(session)
            schedulerService = SchedulerService(session)

            self._copy_scheds_id = []
            for dd in range(7):
                date = self.view._copy_date + datetime.timedelta(days= dd)

                day = dayService.find(date= date)

                if day:
                    scheds = schedulerService.find_all(day= day)
                    for sched in scheds: self._copy_scheds_id.append(sched.id)
        pass

    def on_copy_day_schedules(self):
        with get_db() as session:
            dayService = DayService(session)
            schedulerService = SchedulerService(session)

            day = dayService.find(date= self.view._copy_date)
            
            self._copy_scheds_id = []
            if day:
                scheds = schedulerService.find_all(day= day)

                for sched in scheds:
                    self._copy_scheds_id.append(sched.id)
        pass

    def on_paste_schedules(self):
        if self.view.bulk_mode == 'week': self.__paste_week()
        if self.view.bulk_mode == 'day': self.__paste_day()

        self.page.pubsub.send_all_on_topic('table-update', None)
        pass

    def on_remove_schedules(self):
        if self.view.bulk_mode == 'day': 
            self.__remove_day(date= self.view._copy_date)

        if self.view.bulk_mode == 'week': 
            for dd in range(7):
                date = self.view.date_week + datetime.timedelta(days=dd)
                self.__remove_day(date= date)

        self.page.pubsub.send_all_on_topic('table-update', None)
        pass

    def __paste_week(self):
        with get_db() as session:
            schedulerService = SchedulerService(session)
            date = self.view._copy_date

            try:
                #Mapping new days
                _week_scheds = []
                _days = {}
                for dd in range(7):
                    _date = date + datetime.timedelta(days= dd)
                    _day = self.__get_day(date= _date)

                    _scheds = schedulerService.find_all(day= _day)
                    _week_scheds.extend(_scheds)
                    _days[_date.isoweekday()] = _day
                
                #Deleting schedules from new days
                for _sched in _week_scheds:
                    schedulerService.delete(id= _sched.id)

                #Copy
                for id in self._copy_scheds_id:
                    sched = schedulerService.find(id= id)
                    day = _days[sched.day.date.isoweekday()]

                    schedulerService.create(
                        day= day,
                        hour= sched.hour,
                        begin= sched.begin,
                        annotation= sched.annotation,
                        task= sched.task,
                        priority= sched.priority
                    )
            except UnknownError as error:
                raise error
            except Exception:
                raise UnknownError('__paste_week()')
        pass

    def __paste_day(self):
        with get_db() as session:
            schedulerService = SchedulerService(session)
            date = self.view._copy_date
            try:
                day = self.__get_day(date= date)

                scheds = schedulerService.find_all(day= day)
                for sched in scheds: schedulerService.delete(id= sched.id)

                for id in self._copy_scheds_id:
                    copy = schedulerService.find(id= id)

                    schedulerService.create(
                        day= day,
                        hour= copy.hour,
                        annotation= copy.annotation,
                        begin= copy.begin,
                        task= copy.task,
                        priority= copy.priority
                    )
            except UnknownError as error:
                raise error
            except Exception:
                raise UnknownError('__paste_day()')
        pass

    def __remove_day(self, date):
        with get_db() as session:
            dayService = DayService(session)
            schedulerService = SchedulerService(session)

            try:
                day = dayService.find(date= date)

                if day:
                    scheds = schedulerService.find_all(day= day)
                    for sched in scheds: schedulerService.delete(id= sched.id)
            except Exception:
                raise UnknownError('__remove_day()')
        pass

    def __get_day(self, date):
        with get_db() as session:
            dayService = DayService(session)

            try:
                day = dayService.create(date= date)
            except IntegrityError:
                session.rollback()
                day = dayService.find(date= date)
            except Exception as e: 
                raise UnknownError('__get_day()')
            return day