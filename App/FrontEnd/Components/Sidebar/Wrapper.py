from App.FrontEnd.Components.Models._side  import wrapper, period, hours_container, icon_container
import flet as ft

class Wrapper:
    def __init__(self, father=None) -> None:
        self.father = father
        self.__model = None
        self.__dawn = None
        self.__morning = None
        self.__afternoon = None
        self.__night = None
        self.__hours = None
        self.__hours_container = None
        self._container()
        self._split_hours()

    def _container(self):
        if self.__model is not None: return self.__model
        _father = self.father if isinstance(self.father, ft.Container) else self.father.view
        _model = wrapper(father=_father)

        self.__model = _model

    def _radom(self, mod, add):
        if mod:
            _current = mod.content.controls
            _icon = _current[1]
            _hours = _current[0]

            _hours.content = ft.Column(
                spacing=0,
                controls=add
            )
            return mod

    def _split_hours(self):
        cont = 0
        _hours = []

        if self.__hours:
            for i in range(4):
                list = []
                for j in range(6):
                    curr = self.__hours[cont]
                    hour = curr if isinstance(curr, ft.Container) else curr.view
                    list.append(hour)

                    cont += 1
                _hours.append(list)

        self.__hours = _hours

    def _get_period(self, _period=None):
        _icon_src = {
            'dawn' : r'App\FrontEnd\Resources\Svg\dawn.svg',
            'morning' : r'App\FrontEnd\Resources\Svg\morning.svg',
            'afternoon' : r'App\FrontEnd\Resources\Svg\afternoon.svg',
            'night' : r'App\FrontEnd\Resources\Svg\night.svg'
        }
        _content = []
        if self.__hours:
            _hrs = {
                'dawn' : 0,
                'morning' : 1,
                'afternoon' : 2,
                'night' : 3,
            }
            curr = _hrs[_period]
            _content = self.__hours[curr]
            

        _father = self.__model
        _container = period(father=_father)
        _hours = hours_container(father=_container)
        _icon = icon_container(father=_container, src=_icon_src[_period])
        

        _hours.content = ft.Column(
             spacing=0,
             controls=_content
        )

        _controls = []
        if _hours: _controls.append(_hours)
        if _icon: _controls.append(_icon)

        _container.content = ft.Row(
            spacing=0,
            controls=_controls
        )
        return _container

    @property
    def view (self):
        _model = self.__model
        _model.content = ft.Column(
            spacing=0,
            controls=[
                self.dawn,
                self.morning,
                self.afternoon,
                self.night
            ]
        )
        return _model

    @property
    def dawn(self):
        if self.__dawn is not None: return self.__dawn
        _model = self._get_period(_period='dawn')
        self.__dawn = _model
        return _model
    
    @property
    def morning(self):
        if self.__morning is not None: return self.__morning
        _model = self._get_period(_period='morning')
        self.__morning = _model
        return _model

    @property
    def afternoon(self):
        if self.__afternoon is not None: return self.__afternoon
        _model = self._get_period(_period='afternoon')
        self.__afternoon = _model
        return _model

    @property
    def night(self):
        if self.__night is not None: return self.__night
        _model = self._get_period(_period='night')
        self.__night = _model
        return _model
    
    @property
    def hours_container(self):
        if self.__hours_container: return self.__hours_container
        _father = self.__model
        _container = period(father=_father)
        _model = hours_container(father=_container)

        self.__hours_container = _model
        return _model

    @property
    def hours(self):
        return self.__hours
    
    @hours.setter
    def hours(self, val=None):
        self.__hours = val
        self._split_hours()