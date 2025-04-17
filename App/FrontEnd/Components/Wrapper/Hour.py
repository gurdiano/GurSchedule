from App.FrontEnd.Components.Models.models import task, task_content
from App.FrontEnd.Services.Communication import comm

import datetime, flet as ft

preto_menos_preto = '#020202'
preto_com_brancodes = '#0a0a0a' 
gelo = '#e0e0e0'
tipo_vinho = '#3c3537'
pink = '#e91e63'
branco = 'white'
verde = '#4caf50'
preto = 'black'

#PICKER
COR_DO_CARD = preto_com_brancodes
COR_DOS_NUM = gelo
COR_TITULO = pink
COR_DA_LINHA = COR_TITULO
COR_SELEÇÃO =  COR_TITULO
SELC_DESTAQUE = branco

#OUTROS
COR_DE_FUNDO = preto
COR_TASK_CON =  preto_menos_preto
HOVER_TASK_CON = preto_com_brancodes

class Hour:
    def __init__(self, father=None, value=None):
        self.value = value
        self.father = father
        self.__model = None

    def _on_hover(self, e):
            comm.hourmarker_on_hover(
                e=e,
                hour=self.value
            )
            comm.picker_on_hover(
                e=e,
                date=self._get_date(day=self.father.value)
            )
    
    def _on_click(self, e):
        comm.cel_on_click(
             e=e,
             datetime=self._create_datetime(e=e)
        )

        self._fetch()

    def _create_datetime(self, e):
        _day = self._get_date(day=self.father.value)
        _hour = self._get_time(hour=self.value)
        return datetime.datetime.combine(_day, _hour)

    def _get_time(self, hour=None):
         return datetime.time(hour)

    def _get_date(self, day=None):
        _con = {
            7 : 1,
            1 : 2,
            2 : 3,
            3 : 4,
            4 : 5,
            5 : 6,
            6 : 7,
        }

        index = comm.datepicker.value

        index_day = _con[index.isoweekday()]
        index_res = day - index_day
        index_click = index + datetime.timedelta(index_res)
        
        return index_click

    def _fetch(self):
        _father = self.view
        _day = self._get_date(self.father.value)
        _time = self._get_time(self.value)

        _model = task_content(
             father=_father
        )

        _father.content = _model
    
        return print(f'day = {_day} \nhour={_time}')

    @property
    def view(self):
        if self.__model is not None: return self.__model

        _father = self.father if isinstance(self.father, ft.Container) else self.father.view
        _model = task(father= _father, _on_click= self._on_click, _on_hover=self._on_hover)

        self.__model = _model

        return _model