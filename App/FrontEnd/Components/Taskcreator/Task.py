import flet as ft
import time

from App.FrontEnd.Components.Models import _newtask as mod
from App.FrontEnd.Components.Models import _confirmation as btn

MARK_COLOR = '#FFFFFF'
LABEL_SIZE = 9
MARK_SIZE = 24
BLACK_BTN = '#000000'

class Task:
    def __init__(self, father=None, page=None, beginning=None, duration=None, click_event=None) -> None:
        self.father = father
        self.page = page
        self.text = None
        self.beginning = beginning
        self.duration = duration
        self.click_event = click_event
        self.__view = None
        self.__model = None
        self.__header = None
        self.__wrapper = None
        self.__name = None
        self.__priority = None
        self.__buttons = None
        self.__save = None
        self.__discard = None
        self.__modal = None
        self._container()
    
    def _container(self):
        _father = self.father if isinstance(self.father, ft.Container) else self.father.view
        _model = mod.create_task(_father)
        self.__model = _model
        return _model

    def _divider(self):
        _father = self.__wrapper
        _model = mod.divider(_father)

        _f1 = mod.field(_model)
        _f2 = mod.field(_model)
        _f3 = mod.field(_model) 

        _model.content = ft.Row(
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,

            controls=[
                _f1,
                _f2,
                _f3,
            ]
        )

        return {
            'divider' : _model,
            'field_left' : _f1,
            'field_middle' : _f2,
            'field_right' : _f3,
        }

    def _grid_icons(self, father=None):
        _model = mod.grid_icons(father=father)

        _icons = []
        # for i in range(5):
        #     _data = find_icon(session=session, id=i+1)
        #     _icon = mod.priority_icons(
        #         father=_model,
        #         name=_data.name,
        #         src=_data.src,
        #         color=_data.priority.value
        #     )
        #     _icons.append(_icon)

        _plus_btn = mod.priority_icons(
            father=_model,
            name='',
            src=r'App\FrontEnd\Resources\Svg\plus-solid.svg',
            color= BLACK_BTN
        )

        _icons.append(_plus_btn)
        _model.content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=1,
            controls=_icons
        )
        return _model

    def on_input(self, e):
        text = e.control.value
        self.text = text

    def save_on_click(self, e):
        time.sleep(0.1)
        self.clear_overley(e=e)
        self.click_event(
            e=e,
            beginning=self.beginning.value,
            duration=self.duration.value,
            text_input=self.text
        )

    def modal_on_yes(self, e):
        self.page.close(self.modal)
        self.page.update()
        time.sleep(0.1)
        self.clear_overley(e=e)
        
    def modal_on_no(self, e):
        self.page.close(self.modal)

    def discard_on_click(self, e):
        self.page.open(
            self.modal
        )

    def clear_overley(self, e):
        self.page.overlay.clear()
        self.page.update()
    
    def open(self, e):
        _item = self.view
        _bg = mod.background(
            father=self.father,
            event=self.clear_overley
        )
        _stack = ft.Stack(
            alignment=ft.alignment.center,
            controls=[
                _bg,
                _item
            ]
        )
        

        self.page.overlay.append(_stack)
        self.page.update()

    @property
    def view(self):
        if self.__view is not None: return self.__view
        _model = self.__model
        _header = self.header
        _wrapper = self.wrapper

        _d0 = self.name
        _d1 = self.beginning if isinstance(self.beginning, ft.Container) else self.beginning.view
        _d2 = self.duration if isinstance(self.duration, ft.Container) else self.duration.view
        _d3 = self.priority
        _d4 = self.buttons

        _wrapper.content = ft.Column(
            spacing=0,
            controls=[
                _d0,
                _d1,
                _d2,
                _d3,
                _d4
            ]
        )
        _model.content = ft.Column(
            spacing=0,
            controls=[
                _header,
                _wrapper
            ]
        )

        self.__view = _model
        return _model

    @property
    def model(self):
        return self.__model

    @property
    def header(self):
        if self.__header is not None: return self.__header

        _father = self.__model
        _model = mod.header(_father)

        self.__header = _model
        return _model

    @property
    def wrapper(self):
        if self.__wrapper is not None: return self.__wrapper
        _father = self.__model
        _model = mod.wrapper(_father)

        self.__wrapper = _model
        return _model

    @property
    def name(self):
        if self.__name is not None: return self.__name
        _father = self.__wrapper
        _model = mod.name_container(_father)

        _icon = mod.icon(_model)
        _name = mod.name(_model, self.on_input)

        _model.content = ft.Row(
            spacing=15,
            alignment= ft.MainAxisAlignment.CENTER,

            controls=[
                _icon,
                _name
            ]
        )

        self.__name = _model
        return _model
    
    @property
    def priority(self):
        if self.__priority is not None: return self.__priority
        _father = self._divider()
        _model = _father['divider']

        _name = mod.priority(_model)
        _grid = self._grid_icons(father=_model)

        _model.content = ft.Column(
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                _name,
                _grid,
            ]
        )
        self.__priority = _model
        return _model

    @property
    def buttons(self):
        _model = mod.divider(father=self.wrapper)
        _save = btn.add_btn(
            father=_model, 
            event=self.save_on_click
        )
        _cancel = btn.cancel_btn(
            father=_model,
            event=self.discard_on_click
        )
        _model.content = ft.Row(
            alignment=ft.MainAxisAlignment.END,
            controls=[ 
                _cancel,
                _save
            ]
        )
        self.__save = _save
        self.__discard = _cancel
        self.__buttons = _model
        return _model

    @property
    def discard(self):
        if self.__buttons is not None: return self.__buttons
        return self.__discard
    
    @property
    def modal(self):
        if self.__modal is not None: return self.__modal

        _model = btn.confirm_box(
            father=self.discard,
            yes_event=self.modal_on_yes,
            no_event=self.modal_on_no,
        )

        self.__modal = _model
        return _model