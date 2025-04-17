from App.FrontEnd.Services.entities import month_english as mm_en
from App.FrontEnd.Components.Models._side import picker_icon, picker_name

import flet as ft
import datetime

class Datepicker:
    def __init__(self, father=None, page=None, value=None) -> None:
        self.father = father
        self.page = page
        self.value = value
        self.__initial = None
        self.__model = None
        self.__icon = None
        self.__title = None
        self._set_date()

    def _set_date(self):
        if self.value is None: 
            _date = datetime.date.today()
            self.value = _date
            self.__initial = _date
        else:
            self.__initial = self.value

    def _get_father(self):
        return self.father if isinstance(self.father, ft.Container) else self.father.view

    def _get_title(self):
        _date = self.value
        _day = _date.day
        _month = _date.month
        return f'{mm_en[_month]} {_day}'    
    
    def _change_namedate(self, e):
        _date = e.control.value

        _day = _date.day
        _month = _date.month
        _year = _date.year

        self.value = _date
        self.title = self._get_title()
        
    def _call_datepicker(self, e):
        _date = self.value

        _datepicker = ft.DatePicker(
            first_date=datetime.datetime(year=2023, month=1, day=1),
            last_date=datetime.datetime(year=2033, month=1, day=1),
            value=_date,
            on_change=self._change_namedate,
        )

        self.page.open(
            _datepicker
        )

    def on_hover(self, e, value=None):
        _date = value

        self.value = _date if self.value == self.__initial else self.__initial
        self.title = self._get_title()
        pass    

    @property
    def icon(self):
        if self.__icon is not None: return self.__icon

        _model = picker_icon(
            father=self._get_father(),
            event=self._call_datepicker
        )

        self.__icon = _model
        return _model
    
    @property
    def title(self):
        if self.__title is not None: return self.__title

        _model = picker_name(
            father=self._get_father(),
            title=self._get_title(),
            event=self._call_datepicker
        )

        self.__title = _model
        return _model
    
    @title.setter
    def title(self, text=None):
        self.title.content.value = text
        self.title.update()

    @property
    def view(self):
        if self.__model is not None: return self.__model
        title = self.title
        icon = self.icon

        _model = ft.Row(
            spacing=0,
            controls=[
                title,
                icon,
            ]
        )

        self.__model = _model
        return _model
