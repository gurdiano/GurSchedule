from  App.view.components.Timer import Timer
from  App.view.resources.utility.srcs import CLOCK_REGULAR, MOOM_SOLID

from App.dtos.ColumnsDTO import ColumnsDTO
from App.dtos.TimesDTO import TimesDTO

class TimerController:
    def __init__(self, page):
        self.page = page
        self.wakeup_time = None
        self.sleep_time = None

        self.freetimers_control = []
        self.sleeptimers_control = []
        self.freetimers_view = {}
        self.sleeptimers_view = {}

        self.__controls_gen()

    def __controls_gen(self):
        for n in range(7):
            n_column = n + 1
            freetimer_view = Timer(self, self.page, 'free', n_column)
            sleeptimer_view = Timer(self, self.page, 'sleep', n_column)

            self.freetimers_view[n_column] = freetimer_view
            self.sleeptimers_view[n_column] = sleeptimer_view
            self.freetimers_control.append(freetimer_view)
            self.sleeptimers_control.append(sleeptimer_view)
        pass
        
    def time_values_handler(self, topic, message: TimesDTO):
        self.sleep_time = message.begin_time
        self.wakeup_time = message.end_time
        pass

    def load_timer_displays(self):
        for n in range(7):
            n_column = n + 1
            self.page.pubsub.send_all_on_topic('timer-display', n_column)
        pass

    def load_timer_display_handler(self, topic, message: ColumnsDTO):
        curr_busy = set()
        nex_busy = set()
        for i in range(len(message.current)):
            _current = message.current[i]
            _next = message.next[i]
            if _current.content != None: curr_busy.add(_current.data['row'])
            if _next.content != None: nex_busy.add(_next.data['row'])

        ini_hour  = self.wakeup_time.hour 
        end_hour = self.sleep_time.hour 

        free_time = end_hour - (ini_hour + 1)
        for n in range(ini_hour, end_hour, 1):
            if n in curr_busy: free_time -= 1

        sleep_time = ((23 - end_hour) + 1) + (ini_hour + 1)
        sleep_rows = []
        for n in range(end_hour, 24, 1):
            if n in curr_busy: sleep_time -= 1
            sleep_rows.append(message.current[n])

        for n in range(0, (ini_hour + 1), 1):
            if n in nex_busy: sleep_time -= 1
            sleep_rows.append(message.next[n])

        free_view = self.freetimers_view[message.n_column]
        sleep_view = self.sleeptimers_view[message.n_column]

        free_view.update_timer(free_time)
        sleep_view.update_timer(sleep_time, sleep_rows)
        pass