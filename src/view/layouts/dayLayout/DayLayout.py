import flet as ft

from view.resources.utility import dividers, convs, colors, fontsize

#Overlay
class DayLayout(ft.Container):
    def __init__(self, app_layout=None, table_column=None, title_bar=None, free_timer=None, sleep_timer=None, date_picker=None, n=None):
        super().__init__()
        self.table_column = table_column
        self.title_bar = title_bar
        self.free_timer = free_timer
        self.sleep_timer = sleep_timer
        self.date_picker = date_picker
        self.n = n
        self.app_layout = app_layout

        self.width = dividers.DAY_LAYOUT_WIDTH + dividers.TITLE_BAR_WIDTH
        self.height = dividers.DAY_LAYOUT_HEIGHT

        self.content = ft.Row(
            spacing= 0,
            controls= [
                ft.Column(
                    controls= [
                        ft.Container(
                            height= self.height * dividers.ROW1,
                            on_click= self.picker_click,
                        ),
                    ],
                    width= dividers.APP_LAYOUT_WIDTH * dividers.COL1,
                    height= dividers.DAY_LAYOUT_HEIGHT,
                    spacing= 0,
                ),
                ft.Column(
                    controls=[
                        ft.WindowDragArea(
                            self.day_label(),
                            maximizable= False,
                        ),
                        self.table_column,
                        self.free_timer,
                        sleep_timer,
                    ],
                    width= dividers.APP_LAYOUT_WIDTH * dividers.COL2,
                    height= dividers.DAY_LAYOUT_HEIGHT,
                    spacing= 0,
                ),
                ft.Column(
                    controls= [
                        ft.Container(
                            bgcolor= colors.BLACK_0,
                            content= title_bar,
                        ),
                    ],
                    width= dividers.TITLE_BAR_WIDTH,
                    height= dividers.TITLE_BAR_HEIGHT,
                    spacing= 0,
                ),
            ],
        )
    
    def picker_click(self, e):
        self.app_layout.row_click()
        self.date_picker.on_click(e)
        pass
    
    def day_label(self):
        day_number = self.n + 1
        text = ft.Text(
            value= convs.name_day(day_number),
            size= fontsize.S1,
            color= colors.WHITE_1,
        )
        return ft.Container(
            width= dividers.APP_LAYOUT_WIDTH * dividers.COL2,
            height= self.height * dividers.ROW1,
            bgcolor= colors.BLACK_0,
            alignment= ft.alignment.center,
            data= day_number,
            content= text,
        )