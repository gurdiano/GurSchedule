import flet as ft

class Table(ft.Container):

    def __init__(self, father, markers, datepicker):
        super().__init__()
        self.father = father
        self.markers = markers
        self.datepicker = datepicker
        self.width = father.width * 0.92
        self.height = father.height * 0.87
