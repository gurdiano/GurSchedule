from  App.view.components.Timer import Timer
from  App.view.resources.utility.srcs import CLOCK_REGULAR, MOOM_SOLID

class TimerController:
    def __init__(self, page):
        self.page = page
        self.freetimers_control = [*[Timer(self, page, '8h', CLOCK_REGULAR) for n in range(7)]]
        self.sleeptimers_control = [*[Timer(self, page, '8h', MOOM_SOLID) for n in range(7)]]