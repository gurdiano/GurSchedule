from App.view.components.Table import Table

from App.model.services import SchedulerService
from App.model.services import DayService

from App.dtos.DisplayDTO import DisplayDTO

from App.model.config import get_db

import datetime

class TableController:
    def __init__(self, page):
        self.page = page
        self.view = Table(self, page)

        self.page.pubsub.subscribe_topic('date-update', self.date_update_handler)    
    
    def on_load_scheds(self, first_date, last_date):
        with get_db() as session:
            schedService = SchedulerService(session)
            dayService = DayService(session)

            delta = (last_date - first_date).days + 1
            dates = [first_date + datetime.timedelta(days= n) for n in range(delta)]

            scheds = []
            for date in dates:
                day = dayService.find(date= date)

                if day:
                    _scheds = schedService.find_all(day=day)
                    scheds.extend(_scheds if _scheds else [])


            for sched in scheds:
                sched_id = sched.id
                control_name = f'{sched.day.date}-{sched.hour}'

                control = self.view.rows_map[control_name]
                self.page.pubsub.send_all_on_topic('sched-load', DisplayDTO(sched_id= sched_id, parent=control))
            pass
    
    def on_highlight_marker(self, e, row, date):
        self.page.pubsub.send_all_on_topic(f'markers/{row}', e)
        self.page.pubsub.send_all_on_topic(f'picker', date)
        pass

    def row_on_click(self, data):
        self.page.pubsub.send_all_on_topic('row-onclick', data)
        pass

    def date_update_handler(self, topic, message):
        self.view.load_scheds(message)
        pass