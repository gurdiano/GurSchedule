import datetime
from view.components.Table import Table

from model.services import SchedulerService
from model.services import DayService

from dtos.DisplayDTO import DisplayDTO
from dtos.ColumnsDTO import ColumnsDTO
from dtos.RowDTO import RowDTO

from model.config import get_db

class TableController:
    def __init__(self, page):
        self.page = page
        self.view = Table(self, page)
    
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

            res = {}
            for sched in scheds:
                control_name = f'{sched.day.date}-{sched.hour}'
                control = self.view.rows_map[control_name]
                sched_id = sched.id

                if control not in res:
                    res[control] = [sched_id]
                else:
                    res[control].append(sched_id)

            self.page.pubsub.send_all_on_topic('sched-queue', len(res))
            for control in res:
                self.page.pubsub.send_all_on_topic('sched-load', DisplayDTO(scheds_id= res[control], parent=control))
            pass
    
    def on_highlight_marker(self, e, row, date):
        self.page.pubsub.send_all_on_topic(f'markers/{row}', e)
        self.page.pubsub.send_all_on_topic(f'picker', date)
        pass

    def row_load_handler(self, topic, message: RowDTO):
        with get_db() as session:
            schedulerService = SchedulerService(session)
            dayService = DayService(session)

            date = message.date
            hour = message.time.hour

            control_name = f'{date}-{hour}'
            if control_name in self.view.rows_map:
                control = self.view.rows_map[control_name]

                day = dayService.find(date= date)
                scheds = schedulerService.find_all(day= day, hour= hour)

                scheds_id = []
                for sched in scheds:
                    scheds_id.append(sched.id)

                self.page.pubsub.send_all_on_topic('sched-load', DisplayDTO(scheds_id= scheds_id, parent=control))
        pass

    def row_on_click(self, data):
        self.page.pubsub.send_all_on_topic('row-onclick', data)
        pass

    def date_update_handler(self, topic, message):
        self.view.load_scheds(message)
        pass

    def table_reload_handler(self, topic, message):
        date = self.view.rows[0].data['date']
        self.view.load_scheds(date)
        pass

    def scheds_load_handler(self, topic, message):
        self.view.progress_ring(0.5)
        pass

    def table_get_columns(self, topic, n_column):
        index = n_column - 1
        curr = index
        nex = index + 1 if index != 6 else 0

        current_column = self.view.columns[curr].content.controls
        next_column = self.view.columns[nex].content.controls

        return ColumnsDTO(
            current= current_column,
            next= next_column,
            n_column= n_column,
        )