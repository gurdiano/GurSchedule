from App.FrontEnd.Components.Models import _beginning as beg 
from App.FrontEnd.Components.Models import _newtask as mod

from App.FrontEnd.Services.entities import isoweek_day
from App.FrontEnd.Services.entities import month_english as mm_en
from App.FrontEnd.Services.entities import decimal_tostring as decimal

import datetime
import flet as ft

MARK_COLOR = '#FFFFFF'
LABEL_SIZE = 9
MARK_SIZE = 24

class Beginning:
    def __init__(self, father=None, value=None, page=None) -> None:
        self.father = father
        self.page = page
        self.value = value
        self.__model = None
        self.__view = None
        self.__hour = None
        self.__date = None
        self.__name = None
        self.__day = None
        self.__icon = None
        self._container()
        self._set_datetime()

    def _set_datetime(self):
        if self.value is None: self.value = datetime.datetime.now()

    def _container(self):
        _father = self.father if isinstance(self.father, ft.Container) else self.father.view
        _model = mod.divider(_father)
        self.__model = _model
    
    def _get_hour(self):
        _hh = decimal(self.value.hour) if self.value is not None else None
        _mm = decimal(self.value.minute) if self.value is not None else None

        return f'{_hh} : {_mm}'
 
    def _get_date(self):
        _date = self.value

        _day = _date.day if self.value is not None else None
        _month = _date.month if self.value is not None else None
        _dweek = _date.weekday() if self.value is not None else None

        return f'{isoweek_day[_dweek]}., {mm_en[_month]} {_day}.'   

    def update_value(self, e, datetime=None):
        _value = datetime
        self.value = _value

        _str_hr = self._get_hour()
        _hour = self.hour
        _hour.value = _str_hr
        _hour.update()

        _str_dt = self._get_date()
        _date = self.date
        _date.value = _str_dt
        _date.update()

    def handle_date_change(self, e: ft.ControlEvent):
        _value = e.control.value
        self.value = _value

        _str_hr = self._get_hour()
        _hour = self.hour
        _hour.value = _str_hr
        _hour.update()

        _str_dt = self._get_date()
        _date = self.date
        _date.value = _str_dt
        _date.update()

    @property
    def view(self):
        if self.__view is not None: return self.__view
        _model = self.__model

        _f1 = self.name
        _f2 = self.day
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
    def name(self):
        if self.__name is not None: return self.__name
        _father = self.__model
        _hour = self.hour
        _model = mod.field(father=_father)

        _name = beg.beginning(_model, _hour)
        _model.content = _name

        self.__name = _model
        return _model
    
    @property
    def hour(self):
        if self.__hour is not None: return self.__hour
        _str = self._get_hour()
        _model = ft.Text(
            _str,
            color=MARK_COLOR,
            size=MARK_SIZE
        )

        self.__hour = _model
        return _model
    
    @property
    def date(self):
        if self.__date is not None: return self.__date
        _model =  ft.Text(
            self._get_date(),
            size=LABEL_SIZE,
            color='white'
        )

        self.__date = _model
        return _model

    @property
    def day(self):
        if self.__day is not None: return self.__day
        _father = self.__model
        _date = self.date
        _model = mod.field(father=_father)
        _day = beg.day(father=_model, date=_date)

        _model.content = _day

        self.__day = _model
        return _model

    @property
    def icon(self):
        if self.__icon is not None: return self.__icon
        _father = self.__model
        _model = mod.field(father=_father)
        _icon = beg.icon2(_model, self.page, self.handle_date_change)

        _model.content = _icon

        self.__icon = _model
        return _model
