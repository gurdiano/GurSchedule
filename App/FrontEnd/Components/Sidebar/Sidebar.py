
from App.FrontEnd.Components.Models._side import side_bar
from App.FrontEnd.Components.Models.models import header, footer

import flet as ft

preto_com_brancodes = '#0a0a0a' 
COR_DO_CARD = preto_com_brancodes

class Sidebar:
    def __init__(self, father=None) -> None:
        self.father = father
        self.datepicker = None
        self.content = None
        self.__model = None
        self.__header = None
        self.__wrapper = None
        self.__footer = None
        self._container()

    def _container(self):
        _father = self.father if isinstance(self.father, ft.Container) else self.father.view
        self.__model = side_bar(father= _father)

    @property
    def view(self) :
        _model = self.__model
        _header = self.header
        _wrapper = self.wrapper
        _footer = self.footer

        _controls = []
        if _header is not None: _controls.append(_header)
        if _wrapper is not None: _controls.append(_wrapper)
        if _footer is not None: _controls.append(_footer)

        _model.content = ft.Column(
            spacing=0,
            controls=_controls
        )
        return _model

    @property
    def header(self):
        if self.__header is not None: return self.__header

        _father = self.__model
        _model = header(father= _father)

        _model.width -= 1
        _model.height -= 1
        _model.bgcolor = COR_DO_CARD
        _model.border = ft.border.all(0.5, COR_DO_CARD)
        _model.border_radius = ft.border_radius.all(3)

        self.__header = _model
        return _model

    @header.setter
    def header(self, datepicker=None):
        self.header.content = datepicker.view
        return self.view

    @property
    def wrapper(self):
        return self.__wrapper

    @wrapper.setter
    def wrapper(self, obj):
        self.content = obj
        self.__wrapper = obj.view

    @property
    def footer(self):
        if self.__footer is not None: return self.__footer

        _father = self.__model
        _model = footer(father= _father)

        self.__footer = _model
        return _model
    


