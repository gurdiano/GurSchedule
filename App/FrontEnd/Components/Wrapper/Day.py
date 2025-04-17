from App.FrontEnd.Components.Models.models import grade_day

import flet as ft

class Day:
    def __init__(self, father=None, value=None) -> None:
        self.value = value
        self.father = father
        self.__model = None
    
    @property
    def view(self):
        if self.__model is not None: return self.__model
        _father = self.father if isinstance(self.father, ft.Container) else self.father.view
        _model = grade_day(father= _father)
        
        self.__model = _model
        return _model