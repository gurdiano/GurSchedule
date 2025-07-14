import flet as ft

from view.resources.utility import dividers, colors, fontsize, srcs, convs
from view.layouts.fullWeekLayout.Header import Header
from view.layouts.fullWeekLayout.Body import Body
from view.components.Alerts import Alerts

class Bulk:
    def __init__(self, controller, page):
        self.controller = controller
        self.page = page
        self.date_week = None

        self.EDITOR_WIDTH = dividers.APP_LAYOUT_WIDTH * 0.20
        self.EDITOR_HEIGHT = dividers.APP_LAYOUT_HEIGHT * 0.15
        self.THEME_HOVER = convs.lucidity_color('1a', colors.CTHEME_1)

        self._border_0 = ft.border.BorderSide(0.5, self.THEME_HOVER)
        self._border_1 = ft.border.BorderSide(2, self.THEME_HOVER)
        self._header_border_std = ft.border.only(
            left= self._border_0,
            top= self._border_0, 
            right=self._border_0
        )
        self._column_border_std = ft.border.only(
            left= self._border_0,
            bottom= self._border_0, 
            right=self._border_0
        )
        self._header_border_hvr = ft.border.only(
            left= self._border_1, 
            top= self._border_1, 
            right=self._border_1
        )
        self._column_border_hvr = ft.border.only(
            left= self._border_1, 
            bottom= self._border_1, 
            right=self._border_1
        )

        #day or week
        self.bulk_mode = None
        self._editor_mode = None
        self._editor_mode_value = None
        self._selected_view = None
        self._copy_on = False
        self._copy_date = None

        self.alerts = Alerts(page= page)

        self.bgoverlay = ft.Container(
            width= dividers.APP_LAYOUT_WIDTH,
            height= dividers.APP_LAYOUT_HEIGHT,
            bgcolor= '#CC000000',
            on_click= self.__clear_overlay
        )

    def bulk_active(self):
        self.controller.on_bulk_active()
        pass

    def copy_day_schedules(self):
        self.controller.on_copy_day_schedules()
        pass

    def copy_week_schedules(self):
        self.controller.on_copy_week_schedules()
        pass

    def paste_schedules(self):
        self.controller.on_paste_schedules()
        pass

    def remove_schedules(self):
        self.controller.on_remove_schedules()
        pass

    def close_editor(self, e):
        self.page.overlay.clear()
        self.page.update()
        self.bulk_active()
        pass

    def next_week(self):
        self.controller.on_next_week()
        pass

    def back_week(self):
        self.controller.on_back_week()
        pass

    def update_overlay(self):
        color = convs.lucidity_color('33', colors.CTHEME_1)

        if self._copy_on:
            if self.bulk_mode == 'day':
                header = self._selected_view['header']
                column = self._selected_view['column']

                if convs.date_between(self.date_week ,self._copy_date):
                    header.bgcolor = color
                    column.bgcolor = color
                    header.on_hover = None
                    column.on_hover = None
                    header.update()
                    column.update()
                    return
                
                header.bgcolor = colors.BLACK_0
                column.bgcolor = None
                header.on_hover = lambda e: self.__layout_column_hover(e, header, column) 
                column.on_hover = lambda e: self.__layout_column_hover(e, header, column) 
                header.update()
                column.update()
            
            if self.bulk_mode == 'week':
                view = self._selected_view

                if self._copy_date == self.date_week:
                    view.bgcolor = color 
                    view.update()
                    return
                
                view.bgcolor = None
                view.update()
        pass

    def open_copy_bulk(self):
        window = self._schedule_bulk_build()
        self.__open(window)
        pass

    def open_bulk_edit(self):
        mode = self.bulk_mode
        self._selected_view = None
        self._copy_on = False

        overlay = None
        if mode == 'day': overlay = self._layout_overlay_build()
        if mode == 'week': overlay = self._week_overlay_build()

        editor = self._bulk_editor_build()

        self.page.overlay.append(
            ft.Stack(
                controls= [
                    overlay,
                    editor,
                ],
                alignment= ft.alignment.bottom_right,
                width= dividers.APP_LAYOUT_WIDTH,
                height= dividers.APP_LAYOUT_HEIGHT,
            )
        )

        self.page.update()
        self.bulk_active()
        pass

    def _layout_overlay_build(self):
        overlay = ft.Container(
            width= dividers.APP_LAYOUT_WIDTH,
            height= dividers.APP_LAYOUT_HEIGHT,
        )
        header = self.__layout_header(overlay)
        body = self.__layout_body(overlay)
        
        date_picker = header.controls.pop(0)
        for n in range(len(header.controls)):
            _header = header.controls[n]
            _column = body.table.controls[n]
            self.__set_layout_events(_header, _column)
        header.controls.insert(0, date_picker)

        overlay.content = ft.Column(
            controls= [
                header,
                body,
            ],
            spacing= 0,
            alignment= ft.MainAxisAlignment.START,
        )
        return overlay
    
    def _week_overlay_build(self):
        border_0 = ft.border.all(1, self.THEME_HOVER)
        border_1 = ft.border.all(2, self.THEME_HOVER)

        overlay = ft.Container(
            width= dividers.APP_LAYOUT_WIDTH,
            height= dividers.APP_LAYOUT_HEIGHT,
        )

        def on_hover(e):
            con = e.control
            con.border = border_1 if con.border == border_0 else border_0
            con.bgcolor = self.THEME_HOVER if con.bgcolor == None else None
            con.update()
        
        def on_click(e):
            con = e.control

            if self._selected_view and self._editor_mode_value == 'Copy':
                self._paste_scheds()
                self._selected_view = None
                con.bgcolor = self.THEME_HOVER
                con.on_hover = on_hover
                con.update()
                return
            
            if self._editor_mode_value == 'Remove':
                if self._selected_view:
                    self._selected_view = None
                    con.bgcolor = self.THEME_HOVER
                    con.on_hover = on_hover
                    con.update()
                return self._delete_scheds()
            
            self._selected_view = con
            self._copy_scheds()
            con.bgcolor = convs.lucidity_color('33', colors.CTHEME_1) 
            con.on_hover = None
            con.update()

        column_week = ft.Container(
            width= dividers.APP_LAYOUT_WIDTH * dividers.COL4,
            height= (dividers.APP_LAYOUT_HEIGHT * dividers.ROW1) + (dividers.APP_LAYOUT_HEIGHT * dividers.ROW2),
            border= border_0,
            on_hover= on_hover,
            on_click= on_click,
        )

        overlay.content = ft.Row(
            controls= [
                ft.Column(
                    width= dividers.APP_LAYOUT_WIDTH * dividers.COL1,
                    height= dividers.APP_LAYOUT_HEIGHT,

                    controls= [
                        #date_picker
                        ft.Container(
                            width= dividers.APP_LAYOUT_WIDTH * dividers.COL1,
                            height= dividers.APP_LAYOUT_HEIGHT * dividers.ROW1,
                        )
                    ],
                ),
                ft.Column(
                    width= dividers.APP_LAYOUT_WIDTH * dividers.COL4,
                    height= dividers.APP_LAYOUT_HEIGHT,
                    alignment= ft.MainAxisAlignment.START,
                    spacing= 0,

                    controls= [
                        column_week
                    ],
                ),
            ],
            spacing= 0,
            vertical_alignment= ft.CrossAxisAlignment.START
        )
        return overlay

    def _bulk_editor_build(self):
        _width = self.EDITOR_WIDTH
        _height = self.EDITOR_HEIGHT
        btn_width = _width * 0.20
        btn_height = _height * 0.70
        close_height = _height * 0.20
        self._editor_mode = None
        
        def btn(name= None, src= None, color= None, event= None, pag= None):
            def on_hover(e):
                con = e.control
                icon = e.control.content
                
                icon.color = color if icon.color == colors.BLACK_1 else colors.BLACK_1
                con.bgcolor = colors.DEFAULT_1 if con.bgcolor == colors.DEFAULT_0 else colors.DEFAULT_0
                con.update()
            
            def on_click(e):
                if not pag:
                    con = e.control
                    icon = con.content

                    if self._editor_mode:
                        old_view = self._editor_mode
                        old_icon = old_view.content
                        old_view.bgcolor = colors.DEFAULT_0
                        old_icon.color = colors.BLACK_1
                        old_view.on_hover = old_view.data
                        old_view.update()
                    self._editor_mode = con
                    self._editor_mode_value = name
                    
                    icon.color = color
                    con.on_hover = None
                    con.bgcolor = colors.DEFAULT_1
                    con.update()
                if event:
                    event()
            return ft.Column(
                controls= [
                    ft.Container(
                        content= ft.Image(
                            src= src if src else srcs.BAN,
                            fit= ft.ImageFit.CONTAIN,
                            width= btn_height * 0.40,
                            height= btn_height * 0.40,
                            color= colors.BLACK_1,
                        ),
                        width= btn_width,
                        height= btn_height * 0.80,
                        alignment= ft.alignment.center,
                        bgcolor= colors.DEFAULT_0,
                        border= ft.border.all(1, colors.BLACK_3),
                        border_radius= ft.border_radius.all(5),
                        on_hover= on_hover,
                        on_click= on_click,
                        data= on_hover
                    ),
                    ft.Container(
                        content= ft.Text(
                            value= name if name else 'Void',
                            color= colors.WHITE_1,
                            size= fontsize.S4,
                        ),
                        width= btn_width,
                        height= btn_height * 0.20,
                        alignment= ft.alignment.center,
                    )
                ],
                width= btn_width,
                height= btn_height,
                spacing= 0,
            )
        
        btn_copy = btn(
            name= 'Copy',
            src= srcs.PLUS,
            color= colors.CTHEME_1,
        )
        icon = btn_copy.controls[0]
        icon.bgcolor = colors.DEFAULT_1
        icon.content.color = colors.CTHEME_1
        icon.on_hover = None
        self._editor_mode = icon
        self._editor_mode_value = 'Copy'

        return ft.Container(
            content= ft.Column(
                controls= [
                    ft.Row(
                        controls= [
                            ft.Container(
                                content= ft.Image(
                                    src= srcs.X_MARK,
                                    color= 'red',
                                    fit= ft.ImageFit.CONTAIN,
                                    width= close_height * 0.50,
                                    height= close_height * 0.50,
                                ),
                                alignment= ft.alignment.center,
                                margin= ft.margin.only(right= _height * 0.10),
                                on_click= self.close_editor,
                            ),
                        ],
                        width= _width,
                        height= close_height,
                        alignment= ft.MainAxisAlignment.END,
                        vertical_alignment= ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            btn(
                                name= 'Remove',
                                src= srcs.TRASH,
                                color= 'red'
                            ),

                            btn_copy,

                            btn(
                                name= 'Back',
                                src= srcs.CHEVRON_LEFT,
                                color= colors.BLUE_DEFAULT,
                                pag= True,
                                event= self.back_week,
                            ),
                            btn(
                                name= 'Next',
                                src= srcs.CHEVRON_RIGHT,
                                color= colors.BLUE_DEFAULT,
                                pag= True,
                                event= self.next_week,
                            ),
                        ],
                        width= _width,
                        height= _height * 0.80,
                        alignment= ft.MainAxisAlignment.CENTER,
                        vertical_alignment= ft.CrossAxisAlignment.START,
                    ),
                ],
                width= _width,
                height= _height,
                spacing= 0,
            ),
            bgcolor= colors.BLACK_1,
            border= ft.border.all(1, colors.BLACK_3),
            margin= ft.margin.only(bottom= _width * 0.05),
        )

    def _schedule_bulk_build(self):
        WIDTH = dividers.APP_LAYOUT_WIDTH * 0.30
        HEIGHT = dividers.APP_LAYOUT_HEIGHT * 0.30

        def day_on_click(e):
            self.__clear_overlay(e)
            self.bulk_mode = 'day'
            self.open_bulk_edit()

        def week_on_click(e):
            self.__clear_overlay(e)
            self.bulk_mode = 'week'
            self.open_bulk_edit()

        return ft.Container(
            width= WIDTH,
            height= HEIGHT,
            bgcolor= colors.BLACK_1,
            border= ft.border.all(1, colors.BLACK_3),

            content= ft.Column(
                controls = [
                    ft.Row(
                        controls= [
                            ft.Container(
                                content= ft.Row(
                                    controls=[
                                        ft.Text(
                                            value= 'Schedule Bulk',
                                            size= fontsize.S1,
                                            color= colors.CTHEME_1,
                                        ),
                                        ft.Image(
                                            src= srcs.PEN,
                                            fit= ft.ImageFit.CONTAIN,
                                            color= colors.CTHEME_1,
                                            width= HEIGHT * 0.08,
                                            height= HEIGHT * 0.08,
                                        ),
                                    ],
                                ),

                                alignment= ft.alignment.center,
                            ),
                        ],
                        width= WIDTH * 0.90,
                        height= HEIGHT * 0.30,
                        vertical_alignment= ft.CrossAxisAlignment.CENTER
                    ),

                    ft.Column(
                        controls= [
                            ft.Row(
                                    controls= [
                                        ft.Text(
                                            value= 'Choose a schedule type to copy:',
                                            size= fontsize.S2,
                                            color= colors.WHITE_2,
                                            weight= ft.FontWeight.BOLD,
                                        ),
                                    ],
                                    width= WIDTH * 0.85,
                                    height= HEIGHT * 0.20,
                                    vertical_alignment= ft.CrossAxisAlignment.CENTER,
                                ),

                            ft.Container(
                                content= ft.Row(
                                    controls= [
                                        self.__copy_btn(src= srcs.CALENDAR_REGULAR, name= 'Day', on_click= day_on_click),
                                        self.__copy_btn(src= srcs.BOOK, name= 'Week', on_click= week_on_click),
                                    ],
                                    alignment= ft.MainAxisAlignment.CENTER,
                                    spacing= WIDTH * 0.01,
                                ),
                                expand= True,
                                alignment= ft.alignment.top_center,
                            ),
                        ],
                        width= WIDTH * 0.85,
                        height= HEIGHT * 0.70,
                        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                    ),
                ],
                width= WIDTH * 0.90,
                horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                spacing= 0,
            ),
        )

    def _copy_scheds(self, header=None):
        if self.bulk_mode == 'day': 
            self._copy_date = convs.get_date_by_column(header.data, self.date_week)
            self.copy_day_schedules()
        
        if self.bulk_mode == 'week':
            self._copy_date = self.date_week
            self.copy_week_schedules()
            
        self._copy_on = True
        pass

    def _paste_scheds(self, header=None):
        if self.bulk_mode == 'day':
            date = convs.get_date_by_column(header.data, self.date_week)
            old_date = self._copy_date
            if date != old_date:
                self.alerts.open_confirm_bulk(text= 'copy', event= self.paste_schedules)
                self._copy_date = date
                
        if self.bulk_mode == 'week':
            if self._copy_date != self.date_week: 
                self.alerts.open_confirm_bulk(text= 'copy', event= self.paste_schedules)
                self._copy_date = self.date_week

        self._copy_on = False
        pass

    def _delete_scheds(self, header=None):
        if self.bulk_mode == 'day':
            self._copy_date = convs.get_date_by_column(header.data, self.date_week)

        self.alerts.open_confirm_bulk(text= 'remove', event= self.remove_schedules)
        self._copy_on = False

    def __copy_btn(self, src=None, name=None, on_click= None):
        WIDTH = dividers.APP_LAYOUT_HEIGHT * 0.10
        HEIGHT = dividers.APP_LAYOUT_HEIGHT * 0.10

        def on_hover(e):
            con = e.control
            con.bgcolor = colors.CTHEME_1 if con.bgcolor == colors.CDEFAULT else colors.CDEFAULT
            con.update()

        return ft.Container(
            content= ft.Column(
                controls= [
                    ft.Container(
                        content= ft.Image(
                            src= src if src else srcs.BAN,
                            color= colors.WHITE_1,
                            fit= ft.ImageFit.CONTAIN,
                            width= HEIGHT * 0.40,
                            height= HEIGHT * 0.40,
                        ),

                        width= HEIGHT * 0.80,
                        height= HEIGHT * 0.80,
                        bgcolor= colors.CDEFAULT,
                        border_radius= ft.border_radius.all(5),
                        alignment= ft.alignment.center,
                        on_hover= on_hover,
                    ),
                    ft.Container(
                        content= ft.Text(
                            value = name,
                            size= fontsize.S3,
                            color= colors.WHITE_1,
                        ),
                        alignment= ft.alignment.center,
                        width= HEIGHT * 0.80,
                        height= HEIGHT * 0.20,
                    ),
                ],
                spacing= 0,
            ),
            width= WIDTH,
            height= HEIGHT,
            alignment= ft.alignment.center,
            on_click= on_click,
        )

    def __clear_overlay(self, e):
        self.page.overlay.clear()
        self.page.update()
        pass

    def __open(self, content):
        stack = ft.Stack(
            alignment= ft.alignment.center,

            controls= [
                self.bgoverlay,
                content
            ]
        )
        
        self.page.overlay.append(stack)
        self.page.update()
        pass

    def __set_layout_events(self, header, column):
        header.on_hover = lambda e: self.__layout_column_hover(e, header, column)
        column.on_hover = lambda e: self.__layout_column_hover(e, header, column)

        header.on_click = lambda e: self.__layout_column_click(e, header, column)
        column.on_click = lambda e: self.__layout_column_click(e, header, column)
        pass

    def __layout_column_hover(self, e, header, column):
        color = self.THEME_HOVER
        header_bh = self._header_border_hvr
        header_bs = self._header_border_std
        column_bh = self._column_border_hvr
        column_bs = self._column_border_std

        header.bgcolor = color if header.bgcolor == colors.BLACK_0 else colors.BLACK_0
        header.border = header_bh if header.border == header_bs else header_bs
        
        column.bgcolor = color if column.bgcolor == None else None
        column.border = column_bh if column.border == column_bs else column_bs

        header.update()
        column.update()
        pass

    def __layout_column_click(self, e, header, column):
        color = convs.lucidity_color('33', colors.CTHEME_1)
        
        def app_visual(_header, _column):
            _header.bgcolor = self.THEME_HOVER if _header.bgcolor == color else color 
            _column.bgcolor = self.THEME_HOVER if _column.bgcolor == color else color
            _header.update()
            _column.update()
        def rem_visual(_header, _column):
            _header.bgcolor = colors.BLACK_0
            _column.bgcolor = None
            _header.update()
            _column.update()
        def app_hover(_header, _column):
            _header.on_hover = lambda e: self.__layout_column_hover(e, _header, _column)
            _column.on_hover = lambda e: self.__layout_column_hover(e, _header, _column)
        def rem_hover(_header, _column):
            _header.on_hover = None
            _column.on_hover = None

        data = {
            'header': header,
            'column': column,
        }
        if self._selected_view and self._editor_mode_value == 'Copy':
            old_header = self._selected_view['header']
            old_column = self._selected_view['column']

            if old_header != header: 
                self._selected_view = None
                self._paste_scheds(header) # 
                app_hover(old_header, old_column)
                return rem_visual(old_header, old_column)
            
            if old_header == header: 
                self._selected_view = None
                self._paste_scheds(header) #
                app_hover(header, column)
                return app_visual(header, column)
            
        if self._editor_mode_value == 'Remove':
            if self._selected_view:
                old_header = self._selected_view['header']
                old_column = self._selected_view['column']

                self._selected_view = None
                old_header.bgcolor = colors.BLACK_0
                old_column.bgcolor = None
                old_header.update()
                old_column.update()
            return self._delete_scheds(header= header)
            
        self._selected_view = data
        rem_hover(header, column)
        app_visual(header, column)
        self._copy_scheds(header) # 
        pass

    def __layout_header(self, overlay):
        header = Header(
            father= overlay,
            datepicker= None,
        )
        
        header.controls.pop(0)
        for control in header.controls:
            control.border = self._header_border_std
        header.controls.insert(0, header.side)

        return header

    def __layout_body(self, overlay):
        def column(n):
            column_number = n + 1
            return ft.Container(
                width= dividers.TABLE_COLUMN_WIDTH,
                height= dividers.TABLE_HEIGHT,
                border= self._column_border_std,
                data = column_number,
            )
        body = Body(
            father= overlay,
            markers= None,
            table= None,
        )
        table = ft.Row(
            spacing= 0,
            width= dividers.APP_LAYOUT_WIDTH,
            height= dividers.APP_LAYOUT_HEIGHT,
            controls=[*[column(n) for n in range(7)]],
        )
        body.table = table
        return body