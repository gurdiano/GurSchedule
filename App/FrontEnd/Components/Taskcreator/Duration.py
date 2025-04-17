from App.FrontEnd.Components.Models import _newtask as mod
from App.FrontEnd.Components.Models import _duration as dur 

import datetime
import flet as ft

MARK_COLOR = '#FFFFFF'
LABEL_SIZE = 9
MARK_SIZE = 24

class Duration:
    def __init__(self, father=None, value=None, page=None) -> None:
        self.father = father
        self.page = page
        self.value = value
        self.__model = None
        self.__view = None
        self.__duration = None
        self.__timerpick = None
        self.__name = None
        self.__icon = None
        self._container()
        self._set_time()

    def _set_time(self):
        if self.value is None: self.value = 0

    def _container(self):
        _father = self.father if isinstance(self.father, ft.Container) else self.father.view
        _model = mod.divider(_father)
        self.__model = _model
    
    def _get_duration(self):
        return f'{self.value}'

    def update_value(self, e):
        self.duration.value = self._get_duration()
        self.duration.update()
        
    def handle_time_change(self, e: ft.ControlEvent):
        _value = e.control.value
        _HOUR =  60
        _hour = _value.hour 
        _minutes = _value.minute
        _duration = (_HOUR * _hour) + _minutes
        
        self.value = _duration
        
        _duration = self.duration
        _duration.value = self._get_duration()
        _duration.update()

    @property
    def view(self):
        if self.__view is not None: return self.__view
        _model = self.__model

        _f1 = self.name
        _f2 = mod.field(father=_model)
        _f3 = self.icon

        _model.content = ft.Row(
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,

            controls=[
                _f1,
                _f2,
                _f3,
            ]
        )

        self.__view = _model
        return _model

    @property
    def duration(self):
        if self.__duration is not None: return self.__duration

        _str = self._get_duration()
        _model = ft.Text(
            _str,
            color=MARK_COLOR,
            size=MARK_SIZE
        )

        self.__duration = _model
        return _model

    @property
    def name(self):
        if self.__name is not None: return self.__name
        _father = self.__model
        _model = mod.field(father=_father)
        _duration = dur.duration(
            father=_model,
            minutes=self.duration
        ) 

        _model.content = _duration
        
        self.__name = _model
        return _model
    
    @property
    def timerpick(self):
        if self.__timerpick is not None: return self.__timerpick

        _model = dur.timerpick(
            time=datetime.time(0),
            on_change_time=self.handle_time_change
        )

        self.__timerpick = _model
        return _model

    @property
    def icon(self):
        if self.__icon is not None: return self.__icon
        _father = self.__model
        _model = mod.field(father=_father)

        _icon = dur.icon3(
            father=_model,
            page=self.page,
            timerpick=self.timerpick
        )

        _model.content = _icon

        self.__icon = _model
        return _model