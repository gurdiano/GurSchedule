from App.FrontEnd.Components.Models._side import hour

import flet as ft

class Hour:
    def __init__(self, father=None, value=None) -> None:
        self.father = father
        self.value = value
        self.__view = None

    @property
    def view(self):
        if self.__view is not None: return self.__view
        _father = self.father if isinstance(self.father, ft.Container) else self.father.view
       
        _model = hour(
            father=_father,
            hr=self.value
        )
        self.__view = _model
        return _model