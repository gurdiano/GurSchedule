from App.view.components.TitleBar import TitleBar
from App.view.resources.utility import colors
from App.dtos.TimesDTO import TimesDTO

import os
import json
import datetime

class TitlebarController:
    def __init__(self, page):
        self.page = page

        self.path = r'App\preferences.json'
        self.data = None
        self.begin_time = None
        self.end_time = None
        self.color_theme = None
        self.changed_theme = False
        self.view = None
        
        self.__load_preferences()

    def options_click_handler(self, topic, message):
        self.view.open_options()
        pass

    def times_load_handler(self, topic, message):
        timesDTO = TimesDTO(begin_time= self.begin_time, end_time= self.end_time)
        self.page.pubsub.send_all_on_topic('times-loaded', timesDTO)
        pass

    def bulk_activated(self, topic, message):
        self.view.copy_bulk_active()
        pass

    def on_build_view(self):
        if self.color_theme != colors.CTHEME_1: 
            colors.CTHEME_1 = self.color_theme
            self.changed_theme = True

        self.view = TitleBar(self, self.page)
        self.view.begin_time = self.begin_time
        self.view.end_time = self.end_time
        self.view.update_timers()
        pass

    def on_options_click(self):
        self.page.pubsub.send_all_on_topic('options-click', None)
        pass

    def on_save_times(self):
        _begin = self.view.begin_time
        _end = self.view.end_time

        self.data['begin-sleep-time'] = [_begin.hour, _begin.minute]
        self.data['end-sleep-time'] = [_end.hour, _end.minute]

        with open(self.path, 'w') as file:
            json.dump(self.data, file, indent=4)

        self.begin_time = _begin
        self.end_time = _end
        
        timesDTO = TimesDTO(begin_time= _begin, end_time= _end)
        self.page.pubsub.send_all_on_topic('table-update', None)
        self.page.pubsub.send_all_on_topic('times-loaded', timesDTO)
        pass

    def on_save_color(self):
        color = self.view.color_theme_value

        colors.CTHEME_1 = color
        self.data['color-theme'] = color
        self.color_theme = color

        with open(self.path, 'w') as file:
            json.dump(self.data, file, indent=4)   

        self.page.pubsub.send_all_on_topic('theme-chang', color)
        pass
    
    def on_resize_window(self):
        self.page.pubsub.send_all_on_topic('resize-window', None)
        pass

    def on_copy_bulk_click(self):
        self.page.pubsub.send_all_on_topic('copy-bulk', None)
        pass

    def on_update_btn_click(self):
        theme_color = self.view.color_theme_value
        self.page.pubsub.send_all_on_topic('scheduler-update', theme_color)
        pass

    def __load_preferences(self):
        if not os.path.exists(self.path):
            standard = {
                'begin-sleep-time' : [22, 0],
                'end-sleep-time' : [7, 0],
                'color-theme' : colors.CTHEME_1
            }

            with open(self.path, 'w') as file:
                json.dump(standard, file, indent=4)
        
        with open(self.path, 'r') as file:
            data = json.load(file)

            _begin = data['begin-sleep-time']
            _end = data['end-sleep-time']
            _color = data['color-theme']

            self.begin_time = datetime.time(_begin[0], _begin[1])
            self.end_time = datetime.time(_end[0], _end[1])
            self.color_theme = _color
            self.data = data

        self.on_build_view()
        pass