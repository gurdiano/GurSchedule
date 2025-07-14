import flet as ft
import time
import datetime

from view.layouts import FullWeekLayout
from view.layouts import DayLayout

from view.resources.utility import dividers, dicts, colors

class AppLayout:
    def __init__(self, controller, page):
        self.controller = controller
        self.page = page

        self.date = datetime.date.today()
        self.layout_mode = 'full'
        self.page.window.width = dividers.APP_LAYOUT_WIDTH + dividers.TITLE_BAR_WIDTH
        self.page.window.height = dividers.APP_LAYOUT_HEIGHT

        self.datepicker = self.controller.datepicker_view()
        self.markers = self.controller.marker_controls()
        self.table = self.controller.table_view()
        self.freetimers = self.controller.freetimer_controls()
        self.sleeptimers = self.controller.sleeptimer_controls()

        self.title_bar = ft.WindowDragArea(
            self.controller.titlebar_view(),
            maximizable= False,
        )
        self.full_week_layout = FullWeekLayout(
            app_layout= self,
            datepicker= self.datepicker,
            markers= self.markers,
            table= self.table,
            freetimers= self.freetimers,
            sleeptimers= self.sleeptimers,
        )
        self.view = ft.Row(
            spacing= 0,
            controls = [
                self.full_week_layout,
                self.title_bar,
            ],
        )
    
    def on_load(self):
        self.controller.layout_on_load()
        pass
    
    def progress_ring(self, color, timer=0.8):
        self.page.overlay.append(
            ft.Container(
                content= ft.ProgressRing(
                    color= color
                ),

                alignment= ft.alignment.center,
                bgcolor= '#80000000'
            )
        )
        self.page.update()
        
        time.sleep(timer)

        self.page.overlay.clear()
        self.page.update()
        pass

    def full_week_layout_overlay(self, timer=0.5):
        left_dif = dividers.APP_LAYOUT_WIDTH - dividers.DAY_LAYOUT_WIDTH
        self.page.window.width = dividers.APP_LAYOUT_WIDTH + dividers.TITLE_BAR_WIDTH
        self.page.window.height = dividers.APP_LAYOUT_HEIGHT
        self.page.window.left = self.page.window.left -left_dif
        self.layout_mode = 'full'

        self.page.overlay.clear()
        self.page.clean()
        self.progress_ring(colors.CTHEME_1, timer)
        self.page.add(self.view)
        return 
    
    def day_layout_overlay(self):
        left_dif = dividers.APP_LAYOUT_WIDTH - dividers.DAY_LAYOUT_WIDTH
        self.page.window.width = dividers.DAY_LAYOUT_WIDTH + dividers.TITLE_BAR_WIDTH
        self.page.window.height = dividers.DAY_LAYOUT_HEIGHT 
        self.page.window.left = self.page.window.left + left_dif
        self.layout_mode = 'day'

        n = dicts.isoweek_day[self.date.isoweekday()] - 1
        
        self.page.overlay.append(
            DayLayout(
                app_layout= self,
                title_bar= self.title_bar,
                table_column= self.table.columns[n],
                free_timer= self.freetimers[n],
                sleep_timer= self.sleeptimers[n],
                date_picker= self.datepicker,
                n= n,
            )
        )
        self.page.update()
        pass

    def date_update(self, date):
        self.date = date
        if self.layout_mode != 'full': self.__resize_standard()
        pass

    def row_click(self):
        if self.layout_mode != 'full': self.__resize_standard()
        return

    def toggle(self):
        if self.layout_mode == 'full': return self.day_layout_overlay()
        if self.layout_mode == 'day': return self.full_week_layout_overlay()
        pass

    def build(self):
        return self.view
    
    def __resize_standard(self):
        block = ft.Container(expand= True, bgcolor='#000000')
        self.page.overlay.append(block)
        self.page.update()

        left_dif = dividers.APP_LAYOUT_WIDTH - dividers.DAY_LAYOUT_WIDTH
        self.page.window.width = dividers.APP_LAYOUT_WIDTH + dividers.TITLE_BAR_WIDTH
        self.page.window.height = dividers.APP_LAYOUT_HEIGHT
        self.page.window.left = self.page.window.left -left_dif
        self.layout_mode = 'full'
        self.page.overlay.clear()
        self.page.overlay.append(block)
        self.page.update()

        self.page.clean()
        self.page.add(self.view)

        time.sleep(0.2)
        self.page.overlay.clear()
        self.page.update()
        pass