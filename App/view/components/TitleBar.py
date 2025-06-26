import flet as ft
import time

from App.view.resources.utility import srcs, dividers, colors, fontsize

class TitleBar(ft.Container):
    def __init__(self, controller, page: ft.Page):
        super().__init__()
        self.controller = controller
        self.page = page
        
        self.width = dividers.TITLE_BAR_WIDTH
        self.height = dividers.TITLE_BAR_HEIGHT
        self.bgcolor = ft.Colors.TRANSPARENT
        self.alignment = ft.alignment.top_center

        self.OPTIONS_WIDTH = dividers.APP_LAYOUT_WIDTH * 0.30
        self.ITEM_HEIGHT = self.OPTIONS_WIDTH * 0.15
        self.OPTIONS_HEIGHT = (self.OPTIONS_WIDTH * 0.08) + self.ITEM_HEIGHT

        self.begin_time = None
        self.end_time = None
        self.color_selected = None
        self.color_theme_value = None
        self._copy_bulk_on = False

        self.begin_time_txt = ft.Text(
            value = '99 : 99',
            color= colors.WHITE_2,
            size= fontsize.S1,
        )
        self.end_time_txt = ft.Text(
            value = '99 : 99',
            color= colors.WHITE_2,
            size= fontsize.S1,
        )

        self.config = self._config_build()
        self.resize = self._resize_build()
        self.close = self._close_build() 
        self.copy_bulk = self._copy_bulk_build()
        self.update_btn = self._update_btn_build()

        self.color_theme_option = self.__option('Theme Color', srcs.PAINT_ROLLER, colors.CTHEME_1, self.open_theme)
        self.sleep_time_option = self.__option('Sleep Time', srcs.BED, colors.WHITE_1, self.open_sleep_time)
        self.options_controls = [self.color_theme_option, self.sleep_time_option]

        self.colors = [
            colors.PINK,
            colors.PURPLE,
            colors.BLUE,
            colors.GREEN,
            colors.YELLOW,
            colors.CYAN,
            colors.ORANGE,
            colors.BLUE_GREY
        ]

        self.options = ft.Container(
            bgcolor= colors.BLACK_1,
            border= ft.border.all(1, colors.BLACK_3),
            width= self.OPTIONS_WIDTH,
            height= self.OPTIONS_HEIGHT + (self.ITEM_HEIGHT * len(self.options_controls)), 
            content= ft.Column(
                spacing= 2,
                width=  self.OPTIONS_WIDTH,
                horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                controls= [
                    ft.Row(
                        controls=[
                            ft.Container(
                                content= ft.Row(
                                    controls = [
                                        ft.Image(
                                            src= srcs.GEAR,
                                            color= colors.WHITE_2,
                                            fit= ft.ImageFit.CONTAIN,
                                            width= 10,
                                            height= 10,
                                        ),
                                        ft.Text(
                                            value= 'Settings',
                                            color= colors.WHITE_2,
                                            size= fontsize.S2_02,
                                        ),
                                    ],
                                    spacing= 2,
                                    alignment= ft.MainAxisAlignment.CENTER,
                                ),
                                expand= True,
                                alignment= ft.alignment.center,
                            ),
                            ft.Container(
                                content= ft.Image(
                                    src= srcs.X_MARK,
                                    color= 'red',
                                    fit= ft.ImageFit.CONTAIN,
                                    width= 10,
                                    height= 10,
                                ),
                                height= self.ITEM_HEIGHT,
                                padding= ft.padding.only(top=self.OPTIONS_WIDTH * 0.05),
                                alignment= ft.alignment.top_center,
                            ),
                        ],
                        spacing= 0,
                        width= self.OPTIONS_WIDTH * 0.90,
                        height= self.OPTIONS_WIDTH * 0.15,
                        alignment= ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        controls= self.options_controls,
                        spacing= 2,
                    )
                ],
            ),
        )
        self.sleep_time = ft.Container(
            bgcolor= colors.BLACK_1,
            border= ft.border.all(1, colors.BLACK_3),
            width= self.OPTIONS_WIDTH,
            height= self.OPTIONS_HEIGHT + (self.ITEM_HEIGHT * 4), 
            content= ft.Column(
                spacing= 2,
                width=  self.OPTIONS_WIDTH,
                horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                controls= [
                    ft.Row(
                        controls=[
                            ft.Container(
                                content= ft.Row(
                                    controls = [
                                        ft.Image(
                                            src= srcs.GEAR,
                                            color= colors.WHITE_2,
                                            fit= ft.ImageFit.CONTAIN,
                                            width= 10,
                                            height= 10,
                                        ),
                                        ft.Text(
                                            value= 'Sleep Time',
                                            color= colors.WHITE_2,
                                            size= fontsize.S2_02,
                                        ),
                                    ],
                                    spacing= 2,
                                    alignment= ft.MainAxisAlignment.CENTER,
                                ),
                                expand= True,
                                alignment= ft.alignment.center,
                            ),
                            ft.Container(
                                content= ft.Image(
                                    src= srcs.X_MARK,
                                    color= 'red',
                                    fit= ft.ImageFit.CONTAIN,
                                    width= 10,
                                    height= 10,
                                ),
                                height= self.ITEM_HEIGHT,
                                padding= ft.padding.only(top=self.OPTIONS_WIDTH * 0.05),
                                alignment= ft.alignment.top_center,
                            ),
                        ],
                        spacing= 0,
                        width= self.OPTIONS_WIDTH * 0.90,
                        height= self.OPTIONS_WIDTH * 0.15,
                        alignment= ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls= [
                            ft.Text(
                                value= ' Set the time you plan sleep:',
                                color= colors.WHITE_2,
                                size= fontsize.S2,
                                weight= ft.FontWeight.BOLD,
                            ),
                        ],
                        width= self.OPTIONS_WIDTH * 0.90,
                        height= self.ITEM_HEIGHT,
                        vertical_alignment= ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls= [
                            ft.Container(
                                content= ft.Image(
                                    src= srcs.BED,
                                    color= colors.WHITE_2,
                                    fit= ft.ImageFit.CONTAIN,
                                    width= self.ITEM_HEIGHT * 0.60,
                                    height= self.ITEM_HEIGHT * 0.60,
                                ),

                                alignment= ft.alignment.center,
                                width= self.ITEM_HEIGHT,
                                height= self.ITEM_HEIGHT,
                            ),

                            #time_display_begin
                            ft.Container(
                                content= self.begin_time_txt,

                                width= self.ITEM_HEIGHT * 2,
                                height= self.ITEM_HEIGHT,
                                alignment= ft.alignment.center,
                                bgcolor= colors.BLACK_0,
                                border= ft.border.all(1, colors.BLACK_3),
                                tooltip= 'Example: Monday - 23h...',
                                on_click= lambda e: self.open_clock(e, 'begin', self.begin_time, self.begin_time_txt),
                            ),
                            #time_display_end
                            ft.Container(
                                content= self.end_time_txt,

                                width= self.ITEM_HEIGHT * 2,
                                height= self.ITEM_HEIGHT,
                                alignment= ft.alignment.center,
                                bgcolor= colors.BLACK_0,
                                border= ft.border.all(1, colors.BLACK_3),
                                tooltip= 'Example: Tuesday - 07h...',
                                on_click= lambda e: self.open_clock(e, 'end', self.end_time, self.end_time_txt),
                            )
                        ],

                        width= self.OPTIONS_WIDTH * 0.90,
                        height= self.ITEM_HEIGHT * 1.5,
                        alignment= ft.MainAxisAlignment.CENTER,
                        vertical_alignment= ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls = [
                            ft.Text(
                                value= 'The selected sleep period cannot exceed 24 hours.',
                                size= fontsize.S2,
                                color= 'red'
                            ),
                        ],
                        visible= False,
                        width= self.OPTIONS_WIDTH * 0.90,
                    ),
                    ft.Row(
                        controls=[
                            self.__cancel_btn(event= self.close_dialog),
                            self.__confirm_btn(event= self.save_times),
                        ],
                        width= self.OPTIONS_WIDTH * 0.90,
                        height= self.ITEM_HEIGHT * 2,
                        alignment= ft.MainAxisAlignment.END,
                        vertical_alignment= ft.CrossAxisAlignment.CENTER,
                    ),
                ],
            ),
        )
        self.theme_cfg = ft.Container(
            bgcolor= colors.BLACK_1,
            border= ft.border.all(1, colors.BLACK_3),
            width= self.OPTIONS_WIDTH,
            height= self.OPTIONS_HEIGHT + (self.ITEM_HEIGHT * 3), 
            content= ft.Column(
                spacing= 2,
                width=  self.OPTIONS_WIDTH,
                horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                controls= [
                    ft.Row(
                        controls=[
                            ft.Container(
                                content= ft.Row(
                                    controls = [
                                        ft.Image(
                                            src= srcs.GEAR,
                                            color= colors.WHITE_2,
                                            fit= ft.ImageFit.CONTAIN,
                                            width= 10,
                                            height= 10,
                                        ),
                                        ft.Text(
                                            value= 'Theme',
                                            color= colors.WHITE_2,
                                            size= fontsize.S2_02,
                                        ),
                                    ],
                                    spacing= 2,
                                    alignment= ft.MainAxisAlignment.CENTER,
                                ),
                                expand= True,
                                alignment= ft.alignment.center,
                            ),
                            ft.Container(
                                content= ft.Image(
                                    src= srcs.X_MARK,
                                    color= 'red',
                                    fit= ft.ImageFit.CONTAIN,
                                    width= 10,
                                    height= 10,
                                ),
                                height= self.ITEM_HEIGHT,
                                padding= ft.padding.only(top=self.OPTIONS_WIDTH * 0.05),
                                alignment= ft.alignment.top_center,
                            ),
                        ],
                        spacing= 0,
                        width= self.OPTIONS_WIDTH * 0.90,
                        height= self.OPTIONS_WIDTH * 0.15,
                        alignment= ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls= [
                            ft.Text(
                                value= ' Set color theme:',
                                color= colors.WHITE_2,
                                size= fontsize.S2,
                                weight= ft.FontWeight.BOLD,
                            ),
                        ],
                        width= self.OPTIONS_WIDTH * 0.90,
                        height= self.ITEM_HEIGHT,
                        vertical_alignment= ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls= self.__colors_options(self.colors),
                        width= self.OPTIONS_WIDTH * 0.90,
                        height= self.ITEM_HEIGHT,
                        alignment= ft.MainAxisAlignment.CENTER,
                        vertical_alignment= ft.CrossAxisAlignment.START,
                        spacing= self.OPTIONS_WIDTH * 0.03,
                    ),
                    ft.Row(
                        controls=[
                            self.__cancel_btn(event= self.close_dialog),
                            self.__confirm_btn(event= self.save_color),
                        ],
                        width= self.OPTIONS_WIDTH * 0.90,
                        height= self.ITEM_HEIGHT * 1,
                        alignment= ft.MainAxisAlignment.END,
                        vertical_alignment= ft.CrossAxisAlignment.CENTER,
                    ),
                ],
            ),
        )

        self.content = ft.Column(
            controls= [
                self.close,
                self.resize,
                self.config,
                self.copy_bulk,
                self.update_btn,
            ],

            spacing= 3,
        )
        self.dialog = ft.AlertDialog(
            bgcolor= '#00000000',
            on_dismiss= self.close_dialog,
        )

    def update_timers(self, e=None, u=None):
        if self.begin_time:
            _hour = self.begin_time.hour
            _min = self.begin_time.minute
            self.begin_time_txt.value = f'{_hour if _hour > 9 else f'0{_hour}'} : {_min if _min > 9 else f'0{_min}'}'
        if self.end_time:
            _hour = self.end_time.hour
            _min = self.end_time.minute
            self.end_time_txt.value = f'{_hour if _hour > 9 else f'0{_hour}'} : {_min if _min > 9 else f'0{_min}'}'
        if u:
            self.begin_time_txt.update()
            self.end_time_txt.update()
        pass

    def options_click(self, e):
        self.controller.on_options_click()
        pass

    def save_times(self, e):
        begin = 24 - self.begin_time.hour 
        end = self.end_time.hour + 1

        if begin + end > 24:
            msg_error = self.sleep_time.content.controls[3]
            msg_error.visible = True
            msg_error.update()
            return

        self.sleep_time.content.controls[3].visible = False
        self.page.close(self.dialog)
        self.controller.on_save_times()
        pass

    def save_color(self, e):
        self.page.close(self.dialog)

        if self.color_selected:
            self.color_theme_value = self.color_selected.bgcolor
            self.controller.on_save_color()
        pass
    
    def copy_bulk_click(self, e):
        if self._copy_bulk_on == False: 
            self.controller.on_copy_bulk_click()
        else:
            self.copy_bulk_disabled()
            self.page.overlay.clear()
            self.page.update()
        pass

    def copy_bulk_active(self):
        view = self._copy_bulk_view
        icon = view.content

        view.bgcolor = colors.DEFAULT_1 if view.bgcolor == colors.DEFAULT_0 else colors.DEFAULT_0
        icon.color = colors.CTHEME_1 if icon.color == colors.BLACK_0 else colors.BLACK_0
        self._copy_bulk_on = True if self._copy_bulk_on == False else False
    

        view.on_hover = None if self._copy_bulk_on else lambda e: self.btn_on_hover(e, colors.CTHEME_1)
        
        view.update()
        pass

    def copy_bulk_disabled(self):
        view = self._copy_bulk_view
        icon = view.content

        view.bgcolor = colors.DEFAULT_1
        icon.color = colors.CTHEME_1
        view.on_hover = lambda e: self.btn_on_hover(e, colors.CTHEME_1)

        view.update()
        self._copy_bulk_on = False
        pass

    def update_btn_click(self, e):
        self.controller.on_update_btn_click()
        pass

    def btn_on_hover(self, e, color):
        con = e.control
        icon = con.content

        con.bgcolor = colors.DEFAULT_1 if con.bgcolor == colors.DEFAULT_0 else colors.DEFAULT_0
        icon.color = color if icon.color == colors.BLACK_0 else colors.BLACK_0
        con.update()
        pass

    def open_clock(self, e, mode, time, time_txt):
        def on_change(e):
            _time = timer_picker.value
            hour = _time.hour
            minute = _time.minute

            time_txt.value = f'{hour if hour > 9 else f'0{hour}'} : {minute if minute > 9 else f'0{minute}'}'
            time_txt.update()

            if mode == 'begin': self.begin_time = _time
            if mode == 'end': self.end_time = _time

        timer_picker = ft.TimePicker(
            value= time,
            confirm_text= 'Confirm',
            on_change= on_change,
        )

        self.page.open(timer_picker)

    def close_dialog(self, e):
        self.page.close(self.dialog)
        pass

    def close_window(self, e):
        self.page.window.visible = False
        self.page.update()
        pass

    def resize_window(self, e):
        self.__hover_block()
        self.controller.on_resize_window()
        pass

    def open_options(self):
        self.dialog.content = self.options
        self.options.content.controls[0].controls[1].on_click = self.close_dialog
        self.page.open(self.dialog)
        pass

    def open_sleep_time(self, e):
        self.dialog.content = self.sleep_time
        self.sleep_time.content.controls[0].controls[1].on_click = self.close_dialog
        self.page.open(self.dialog)
        pass

    def open_theme(self, e):
        self.dialog.content = self.theme_cfg
        self.theme_cfg.content.controls[0].controls[1].on_click = self.close_dialog
        self.page.open(self.dialog)
        pass

    def _close_build(self):
        btn = self.__btn(srcs.X_MARK)
        btn.on_hover = lambda e: self.btn_on_hover(e, 'red')
        btn.on_click = self.close_window
        return btn
    
    def _resize_build(self):
        btn = self.__btn(srcs.WINDOW_MAXIMIZE)
        btn.on_hover = lambda e: self.btn_on_hover(e, ft.Colors.BLUE_900)
        btn.on_click = self.resize_window
        return btn
    
    def _config_build(self):
        btn = self.__btn(srcs.GEAR)
        btn.on_hover = lambda e: self.btn_on_hover(e, ft.Colors.BLUE_900)
        btn.on_click = self.options_click
        return btn
    
    def _copy_bulk_build(self):
        btn = self.__btn(srcs.PEN)
        btn.on_hover = lambda e: self.btn_on_hover(e, colors.CTHEME_1)
        btn.on_click = self.copy_bulk_click
        self._copy_bulk_view = btn
        return btn
    
    def _update_btn_build(self):
        btn = self.__btn(srcs.ROTATE_RIGHT)
        btn.on_hover = lambda e: self.btn_on_hover(e, colors.CTHEME_1)
        btn.on_click = self.update_btn_click
        
        return btn
    
    def __hover_block(self):
        hover_block = ft.Container(
            expand= True,
        )

        self.page.overlay.append(hover_block)
        self.page.update()
        time.sleep(0.2)
        self.page.overlay.remove(hover_block)
        self.page.update()
        pass

    def __colors_options(self, colors_list):
        def on_click(e):
            if self.color_selected:
                con = self.color_selected
                con.border = ft.border.all(2, colors.BLACK_3)
                con.update()

            con = e.control
            con.border = ft.border.all(2, colors.WHITE_2)
            con.update()
            self.color_selected = con


        controls = []
        for color in colors_list:
            op = ft.Container(
                bgcolor= color,
                width= self.ITEM_HEIGHT * 0.50,
                height= self.ITEM_HEIGHT * 0.50,
                border= ft.border.all(2, colors.BLACK_3),
                on_click= on_click,
            )
            controls.append(op)
        return controls

    def __confirm_btn(self, event=None):
        return ft.CupertinoButton(
            bgcolor= colors.CTHEME_1,

            width= self.ITEM_HEIGHT * 1.6,
            height= self.ITEM_HEIGHT * 0.80,

            content= ft.Row(
                controls = [
                    ft.Text(
                        value= 'Save',
                        size= fontsize.S1,
                        color= colors.WHITE_1,
                    ),
                    ft.Image(
                        src= srcs.SD_CARD,
                        fit= ft.ImageFit.CONTAIN,
                        width= self.ITEM_HEIGHT * 0.30,
                        height= self.ITEM_HEIGHT * 0.30,
                        color= colors.WHITE_1,
                    ),
                ],

                alignment= ft.MainAxisAlignment.CENTER,
                vertical_alignment= ft.CrossAxisAlignment.CENTER,
                spacing= 5,
            ),

            on_click= event,
        )
    
    def __cancel_btn(self, event=None):
        return ft.CupertinoButton(
            bgcolor= colors.CDEFAULT,
            width= self.ITEM_HEIGHT * 1.6,
            height= self.ITEM_HEIGHT * 0.80,

            content= ft.Row(
                controls = [
                    ft.Text(
                        value= 'Cancel',
                        size= fontsize.S1,
                        color= colors.WHITE_1,
                    ),
                ],
                alignment= ft.MainAxisAlignment.CENTER,
                vertical_alignment= ft.CrossAxisAlignment.CENTER,
                spacing= 5,
            ),
            on_click= event,
        )

    def __option(self, name=None, src=None, color=None, on_click=None):
        WIDTH = self.OPTIONS_WIDTH * 0.90
        HEIGHT = self.ITEM_HEIGHT

        def on_hover(e):
            con = e.control
            con.bgcolor = colors.DEFAULT_0 if con.bgcolor == None else None
            con.update()
        
        def _on_click(e):
            con = e.control
            con.bgcolor = None

        return ft.Container(
            content = ft.Row(
                controls=[
                    ft.Container(
                        content= ft.Image(
                            src= src if src else srcs.BAN,
                            color= color if color else colors.WHITE_2,
                            fit= ft.ImageFit.CONTAIN,
                            width= HEIGHT * 0.40,
                            height= HEIGHT * 0.40,
                        ),
                        width= HEIGHT,
                        height= HEIGHT,
                        alignment= ft.alignment.center,
                    ),

                    ft.Container(
                        content= ft.Text(
                            value= name if name else 'Void',
                            color= colors.WHITE_2,
                            size= fontsize.S2,
                            weight= ft.FontWeight.BOLD,
                        ),
                        alignment= ft.alignment.center_left,
                        expand= True,
                    ),
                ],

                spacing= HEIGHT * 0.20,
            ),
            
            width= WIDTH,
            height= HEIGHT,
            border= ft.border.all(1, colors.DEFAULT_0),
            border_radius= ft.border_radius.all(3),
            on_hover= on_hover,
            on_click= lambda e: [on_click(e), _on_click(e)],
        )

    def __btn(self, src=None):
        return ft.Container(
            width= 25,
            height= 25,
            bgcolor= colors.DEFAULT_0,
            alignment= ft.alignment.center,
            border_radius= ft.border_radius.all(3),
            
            content= ft.Image(
                src= src,
                fit= ft.ImageFit.CONTAIN,
                color= colors.BLACK_0,
                width= 14,
                height= 14,
            )
        )