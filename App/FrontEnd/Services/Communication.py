from App.FrontEnd.Components.Taskcreator.Task import Task
from App.FrontEnd.Components.Taskcreator.Beginning import Beginning
from App.FrontEnd.Components.Taskcreator.Duration import Duration

from App.FrontEnd.Components.Models.models import task_content

preto_menos_preto = '#020202'
preto_com_brancodes = '#0a0a0a'
COR_TASK_CON =  preto_menos_preto
HOVER_TASK_CON = preto_com_brancodes

class Communication:
    def __init__(self, hours=None, datepicker=None, task=None, window=None, page=None) -> None:
        self.hours = hours
        self.datepicker = datepicker
        self.window = window
        self.page = page
        self.omeupiru = 'piru'

    def hourmarker_on_hover(self, e, hour):
        cel_con = e.control
        cel_con.bgcolor = HOVER_TASK_CON if cel_con.bgcolor == COR_TASK_CON else COR_TASK_CON
        
        mark_con = next(hh for hh in self.hours if hh.value == hour)
        mark_con.view.bgcolor = 'pink' if mark_con.view.bgcolor == '#0d0d0d' else '#0d0d0d'

        # cel_con.content = task_content(father=cel_con)

        cel_con.update()
        mark_con.view.update()    

    def picker_on_hover(self, e=None, date=None):
        self.datepicker.on_hover(
            e=e,
            value=date,
        )
        
    def cel_on_click(self, e, datetime=None):
        task = Task(
            father=self.window,
            page=self.page,
            click_event=self.get_info
        )

        beginning = Beginning(
            father=task.model,
            page=self.page,
            value=datetime
        )

        duration = Duration(
            father=task.model,
            page=self.page,
            value=0
        )
        
        task.beginning = beginning
        task.duration = duration
        task.open(e=e)

    def get_info(self, e, beginning=None, duration=None, text_input=None):
        print(f'beginning = {beginning}')
        print(f'duration = {duration}')
        print(f'text_input = {text_input}')

    
comm = Communication()

