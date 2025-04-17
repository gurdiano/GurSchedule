import flet as ft
from App.view.utility.colors import *

class DatePicker(ft.Container):
    def __init__(self, father, txt=None, date=None, display_date=None):
        super().__init__()
        
        self.width = father.width * 0.08
        self.height = father.height * 0.05
        self.bgcolor = black_2
        self.alignment = ft.alignment.center
        self.txt = txt
        self.date = date
        self.display_date = display_date

