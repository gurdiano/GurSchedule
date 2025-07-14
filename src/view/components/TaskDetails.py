import flet as ft
import datetime
import time

from view.resources.utility import colors, srcs, fontsize, dividers
from view.resources.utility.dicts import isoweekday_str, month_english
from flet_contrib.color_picker import ColorPicker

from view.components.Alerts import Alerts

from dtos.SchedDTO import SchedDTO

class TaskDetails (ft.Container):
    def __init__(self, controller, page):
        super().__init__()
        self.controller = controller
        self.page = page
        self.icon = None
        self.name = None
        self.date = None
        self.duration = None
        self.time = None
        self.priority = None
        self.annotation = None

        self.priorities = None
        self.options = None
        self.temp_icon = None
        self.conflicts_id = None

        self.alerts = Alerts(page= self.page)

        self.bgcolor = colors.BLACK_1
        self.width = dividers.APP_LAYOUT_WIDTH * 0.50
        self.height = dividers.APP_LAYOUT_HEIGHT * 0.90
        self.border = ft.border.all(1, colors.BLACK_3)
        self.padding = ft.padding.only(
            top= self.width * 0.06, 
            bottom= self.width * 0.06, 
            left=self.width * 0.05, 
            right=self.width * 0.05
        )

        self.name_input = ft.TextField(
            border= ft.InputBorder.UNDERLINE,
            border_color= colors.WHITE_1,
            width= self.width * 0.20,
            height= (dividers.APP_LAYOUT_HEIGHT * 0.50) * 0.10,
            text_size= fontsize.S1,
            text_align= ft.TextAlign.CENTER,
            text_style= ft.TextStyle(color= colors.CTHEME_1),
            # content_padding= 0,
            on_change= self._name_on_change,
            capitalization= ft.TextCapitalization.SENTENCES,
        )
        self.time_txt = ft.Text(
            '00 : 00',
            color= colors.WHITE_1,
            size= fontsize.S1 * 2,
        )
        self.date_txt = ft.Text(
            'Thu., Oct 0.',
            color= colors.WHITE_1,
            size= fontsize.S4
        )
        self.minute_txt = ft.Text(
            '00',
            color= colors.WHITE_1,
            size= fontsize.S1 * 2,
        )
        self.dropdown = ft.Dropdown(
            label= 'Priorities',
            border_color= colors.WHITE_1,
            border_width= 2,
            menu_width= self.width * 0.40,
            width= self.width * 0.40,
            text_size= fontsize.S2,
            enable_filter= True,
            editable= True,
            menu_height= self.height * 0.40,
            options= [],
            on_change= self.update_priority,
            value= 'DEFAULT',
        )
        self.color_picker_icon = ft.Container(
            border= ft.border.all(2, colors.WHITE_1),
            width= (dividers.APP_LAYOUT_HEIGHT * 0.50) * 0.13,
            height= (dividers.APP_LAYOUT_HEIGHT * 0.50) * 0.13,
            alignment= ft.alignment.center,
            bgcolor= None,
            on_click= self.open_color_picker,
        )
        self.datepicker = ft.Container(
            bgcolor= colors.BLACK_0,
            width= self.width * 0.25,
            border= ft.border.all(1, colors.CDEFAULT),
            border_radius= ft.border_radius.all(3),
            alignment= ft.alignment.center,
            content= ft.Image(
                src= srcs.GEAR,
                fit= ft.ImageFit.CONTAIN,
                color= colors.WHITE_1,
                width= self.width * 0.05,
                height= self.width * 0.05,
            ),
            on_click= self.open_calendar,
            on_hover= lambda e: self._btns_on_hover(e, colors.BLACK_0),
        )
        self.timerpicker = ft.Container(
            bgcolor= colors.BLACK_0,
            width= self.width * 0.25,
            border= ft.border.all(1, colors.CDEFAULT),
            border_radius= ft.border_radius.all(3),
            alignment= ft.alignment.center,
            content= ft.Image(
                src= srcs.STOP_WATCH,
                fit= ft.ImageFit.CONTAIN,
                color= colors.WHITE_1,
                width= self.width * 0.05,
                height= self.width * 0.05,
            ),
            on_click= self.open_watch,
            on_hover= lambda e: self._btns_on_hover(e, colors.BLACK_0),
        )
        self.icon_view = ft.Container(
            bgcolor= colors.BLACK_3,
            width= self.width * 0.25,
            border= ft.border.all(1, colors.BLACK_3),
            border_radius= ft.border_radius.all(3),
            alignment= ft.alignment.center,
            content= ft.Image(
                src= self.icon if self.icon else srcs.BAN,
                fit= ft.ImageFit.CONTAIN,
                color= colors.CTHEME_1,
                width= self.width * 0.05,
                height= self.width * 0.05,
            ),
            on_hover= lambda e: self._icon_btn_on_hover(e, self.color_picker_icon.bgcolor),
            on_click= self.open_all_icons,
        )
        self.annotation_input = ft.TextField(
            text_size= fontsize.S3,
            width= self.width * 0.80,
            border_color= colors.BLACK_3,
            bgcolor= colors.BLACK_3,
            expand= True,
            multiline= True,
            on_change= self._annotation_on_change,
        )

        self.header = ft.Container(
            width= self.width,
            height= (dividers.APP_LAYOUT_HEIGHT * 0.50) * 0.05,
            alignment= ft.alignment.top_left,
            content= ft.Row(
                spacing= 10,
                alignment = ft.MainAxisAlignment.START,
                controls = [
                    ft.Text(
                        'Schedule Task',
                        size= fontsize.S1,
                        color= colors.CTHEME_1,
                        weight= ft.FontWeight.W_600,
                    ),
                    ft.Image(
                        src= srcs.PEN,
                        color=colors.CTHEME_1,
                        fit=ft.ImageFit.CONTAIN,
                        width=(dividers.APP_LAYOUT_HEIGHT * 0.50) * 0.05,
                        height=(dividers.APP_LAYOUT_HEIGHT * 0.50) * 0.05,
                    ),
                ],
            ),
        )
        self.next = ft.CupertinoButton(
            bgcolor=colors.CTHEME_1,
            width=self.width * 0.20,
            height=(dividers.APP_LAYOUT_HEIGHT * 0.50) * 0.15,
            alignment=ft.alignment.center,
            content=ft.Row(
                spacing= self.width * 0.01,
                alignment= ft.MainAxisAlignment.CENTER,
                vertical_alignment= ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        'Save',
                        size=fontsize.S1,
                        color=colors.WHITE_1,
                    ),
                    ft.Image(
                        src=srcs.SD_CARD,
                        fit=ft.ImageFit.CONTAIN,
                        color=colors.WHITE_1,
                        width=(dividers.APP_LAYOUT_HEIGHT * 0.50) * 0.04,
                        height=(dividers.APP_LAYOUT_HEIGHT * 0.50)* 0.04,
                    ),
                ],
            ),
        )
        self.back = ft.CupertinoButton(
            bgcolor=colors.CDEFAULT,
            width=self.width * 0.20,
            height=(dividers.APP_LAYOUT_HEIGHT * 0.50) * 0.15,
            alignment=ft.alignment.center,
            content=ft.Row(
                spacing= self.width * 0.01,
                alignment= ft.MainAxisAlignment.CENTER,
                vertical_alignment= ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(
                        src=srcs.ARROW_LEFT,
                        fit=ft.ImageFit.CONTAIN,
                        color=colors.BLACK_0,
                        width=(dividers.APP_LAYOUT_HEIGHT * 0.50) * 0.04,
                        height=(dividers.APP_LAYOUT_HEIGHT * 0.50) * 0.04,
                    ),
                    ft.Text(
                        'Edit',
                        size=fontsize.S1,
                        color=colors.BLACK_0,
                    ),
                ],
            ),
            visible=True,
        )
        self.name_field = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER, 
            vertical_alignment=ft.CrossAxisAlignment.END,
            width= self.width * 0.80,
            spacing= self.width * 0.03,
            controls=[
                ft.Text(
                    'NAME',
                    size= fontsize.S1,
                    color= colors.WHITE_1,
                ),

                self.name_input,
            ],
        )

        self.color_picker = self._color_picker_build()
        self.date_field = self._date_field_build()
        self.duration_field = self._duration_field_build()
        self.priority_field = self._priority_field_build()
        self.annotation_field = self._annotation_field_build()
        
        self.content = ft.Column(
            controls=[
                self.header,
    
                ft.Container(
                    height= self.height * 0.65,
                    margin= ft.margin.only(top= self.height * 0.03),
                    # border= ft.border.all(1, 'white'),

                    content= ft.Column(
                        spacing= 0,
                        scroll= ft.ScrollMode.ALWAYS,
                        controls= [
                            self.name_field,
                            ft.Container(height= self.height * 0.03),
                            self.date_field,
                            self.duration_field,
                            self.priority_field,
                            self.annotation_field,
                        ],
                    ),
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    expand=True,
                    controls=[
                        self.back,
                        self.next,     
                    ],
                ),
            ],
        )

    def save_sched(self):
        schedDTO = self.__get_data()
        self.controller.on_save_sched(schedDTO)
        pass

    def edit_sched(self):
        schedDTO = self.__get_data()
        self.controller.on_edit_sched(schedDTO)
        pass
    
    def remove_sched(self):
        self.controller.on_remove_sched()
        pass

    def overwrite_sched(self):
        self.controller.on_overwrite_sched(self.__get_data())
        pass

    def load_all_icons(self):
        return self.controller._on_load_all_icons()

    def update_view(self, u=None):
        self.name_input.value = self.name
        self.time_txt.value = self._time_str()
        self.date_txt.value = self._date_str()
        self.minute_txt.value = self._minute_str()
        self.dropdown.value = self.priority['name']
        self.icon_view.content.src = self.icon
        self.__add_priority(self.priority['color'])
        self.color_picker_icon.bgcolor = self.priority['color']
        self.annotation_input.value = self.annotation
        if u:
            self.name_input.update()
            self.time_txt.update()
            self.date_txt.update()
            self.minute_txt.update()
            self.dropdown.update()
            self.icon_view.update()
            self.color_picker_icon.update()
            self.annotation_input.update()

    def creat_priority(self, e):
        text_input = ft.TextField(
            label= 'Name',
            hint_text= 'Default',
            border= colors.WHITE_1,
            width= self.width * 0.40,
            capitalization= ft.TextCapitalization.CHARACTERS,
        )

        def on_dismiss(e):
            last_priority_key = self.priority['name']
            last_priority = self.priorities[last_priority_key]
            text = text_input.value.strip()
            new_priority = None

            if text:
                new_priority = {
                    'name': text,
                    'src': srcs.USER,
                    'color': last_priority['color']
                }

            if new_priority:
                name = new_priority['name']
                icon_src = new_priority['src']

                if name in self.priorities:
                    self.dropdown.value = name
                    self.dropdown.data = name
                    self.priority = new_priority
                    self.update_priority(self.dropdown)
                    self.dropdown.update()
                    return

                new_option = ft.DropdownOption(
                    key= name,
                    text= name,
                    leading_icon= ft.Image(
                        src= icon_src,
                        fit= ft.ImageFit.CONTAIN,
                        width= self.height * 0.04, 
                        height= self.height * 0.04,
                        color= colors.WHITE_2,
                    ),
                    content= ft.Text(
                        name,
                        color= colors.WHITE_2,
                        size= fontsize.S3,
                    ),
                )

                if name not in self.priorities:
                    self.options.insert(1, new_option)
                    self.priority = new_priority
                    self.priorities[name] = new_priority
                    self.dropdown.value = name
                    self.dropdown.update()
            else:
                self.dropdown.value = last_priority_key
                self.dropdown.update()

        def close_dialog(e):
            self.page.close(dialog)
            on_dismiss(e)

        dialog = ft.AlertDialog(
            bgcolor= '#00000000',
            content= ft.Container(
                bgcolor= colors.FLET_DEFAULT,
                width= self.width * 0.45,
                height= self.height * 0.20,
                alignment= ft.alignment.center,
                border_radius= ft.border_radius.all(5),

                content= ft.Column(
                    width= self.width * 0.40,
                    alignment= ft.MainAxisAlignment.CENTER,

                    controls = [
                        ft.Row(
                            alignment= ft.MainAxisAlignment.END,
                            height= self.height * 0.03,

                            controls=[
                                ft.Container(
                                    content= ft.Image(
                                        src= srcs.X_MARK,
                                        color= 'red',
                                        fit= ft.ImageFit.CONTAIN,
                                        width= self.height * 0.03,
                                        height= self.height * 0.03,
                                    ),
                                    alignment= ft.alignment.center_right,
                                    on_click= close_dialog,
                                ),
                            ],
                        ),
                        ft.Text(
                            value= 'Define a name for Priority: ',
                            color= colors.WHITE_1,
                            size= fontsize.S2_02,
                        ),
                        text_input,
                    ],
                ),
            ),
            on_dismiss= on_dismiss,
        )

        self.page.open(dialog)
        pass

    def update_priority(self, e):
            if e.data == 'ADD PRIORITY':
                self.creat_priority(e)
                return

            priority = self.priorities[e.data]
            color = priority['color']

            self.__add_priority(color)

            self.color_picker_icon.bgcolor = color
            self.priority = priority
            self.icon_view.update()
            self.color_picker_icon.update()

    def set_mode(self, action):
        action = action.lower()

        if action == 'creator': self.__mode_creator()
        if action == 'preview': self.__mode_preview()
        if action == 'edit': self.__mode_edit()


        pass

    def set_options(self, priorities):
        def icon(src, color):
            return ft.Image(
                src= src,
                fit= ft.ImageFit.CONTAIN,
                width= self.height * 0.04,
                height= self.height * 0.04,
                color= color,
            )
        def text(name, color):
            return ft.Text(
                name,
                color= color if color else colors.WHITE_2,
                size= fontsize.S3,
            )
        
        options = []
        all_priorities = {}
        for item in priorities:
            options.append(
                ft.DropdownOption(
                    key= item['name'],
                    leading_icon= icon(item['src'], item['color']),
                    content= text(item['name'], item['color']),
                    text= item['name'],
                )
            )
            all_priorities[item['name']] = item
        self.priorities = all_priorities
        
        add_option = ft.DropdownOption(
            key= 'ADD PRIORITY',
            leading_icon= icon(srcs.PLUS, colors.WHITE_1),
            content= text('ADD PRIORITY', colors.WHITE_2),
            text= 'ADD PRIORITY',
        )
        options.insert(0, add_option)

        if self.dropdown.value not in self.priorities:
            name = self.priority['name']
            icon_src = self.priority['src']
            color = self.priority['color']

            new_option = ft.DropdownOption(
                key= name,
                text= name,
                leading_icon= icon(icon_src, color),
                content= text(name, color),
            )
            options.insert(1, new_option)
            self.priorities[name] = self.priority
            
        self.options = options
        pass

    def open_calendar(self, e):
        date = self.date if self.date else datetime.date.today()
        d_week = date.isoweekday()
        i_week = 0 - d_week
        e_week = 6 - d_week

        ini_week = date + datetime.timedelta(days= i_week)
        end_week = date + datetime.timedelta(days= e_week)

        def update_values(e):
            if self.date != datepicker.value:
                self.date = datepicker.value.date()
                
                self.date_txt.value = self._date_str()
                self.date_txt.update()
                self.open_clock(e)
            pass

        datepicker = ft.DatePicker(
            first_date= ini_week,
            last_date= end_week,
            value= date,
            on_change= update_values,
            on_dismiss= self.open_clock,
        )
        self.page.open(
            datepicker
        )

    def open_watch(self, e):
        def update_values(e):
            seconds = cupertino_timer_picker.value

            _value = int(cupertino_timer_picker.value / 60)
            if seconds > 3540 :
                _value = 60

            self.duration = _value if self.time.minute + _value <= 60 else 60 - self.time.minute
            self.minute_txt.value = self._minute_str()
            self.minute_txt.update()

        cupertino_timer_picker = ft.CupertinoTimerPicker(
            value=3541,
            second_interval=10,
            minute_interval=1,
            mode=ft.CupertinoTimerPickerMode.MINUTE_SECONDS,
            on_change=update_values,
        )
        self.page.open(
            ft.CupertinoBottomSheet(
                cupertino_timer_picker,
                height=216,
                padding=ft.padding.only(top=6),
            ),
        )
        pass

    def open_clock(self, e):
        def update_values(e):
            if time_picker.value.minute + self.duration > 60:
                self.duration = 60 - time_picker.value.minute
                self.minute_txt.value = self._minute_str()
                self.minute_txt.update()

            if time_picker.value != self.time:
                self.time = time_picker.value
                self.time_txt.value = self._time_str()
                self.time_txt.update()
        
        time = self.time if self.time else datetime.datetime.now().time()

        time_picker = ft.TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick your time slot",
            value= time,
            on_change= update_values,
        )

        self.page.open(time_picker)
        pass

    def open_color_picker(self, e):
        color_picker_control = self.color_picker.data
        color = color_picker_control.color 
        
        priority = self.priority

        if priority['color'] != None:
            color_picker_control.color = priority['color']
  
        def update_priority_color(e):
            new_color = color_picker_control.color
            if priority['name'] == 'DEFAULT':
                _priority = self.priorities['PERSONAL']
                self.dropdown.value = 'PERSONAL'
                self.dropdown.update()
                self.priority = _priority

            if  new_color != color:
                self.color_picker_icon.bgcolor = new_color
                self.color_picker_icon.update()
                self.icon_view.bgcolor = new_color
                self.icon_view.content.color = colors.WHITE_1
                self.icon_view.update()
                self.priority['color'] = new_color

        self._update_recent_colors_pick()

        self.page.open(
            ft.AlertDialog(
                bgcolor= '#00000000',
                content= self.color_picker,
                on_dismiss= update_priority_color,
            )
        )

    def open_all_icons(self, e):
        all_src = self.load_all_icons()
        self.temp_icon = None

        controls = []
        for n in range(0, len(all_src), 8):
            row = ft.Row(
                spacing= self.width * 0.01,
                alignment= ft.MainAxisAlignment.START,
            )
            for i in range(n, n+8, 1):
                row.controls.append(
                    self._icon_build(all_src[i])
                )
                if i + 1 == len(all_src): break
            controls.append(row)
            
        dialog = ft.AlertDialog(
            bgcolor= colors.FLET_DEFAULT,
        )

        def on_dismiss(e):
            if self.temp_icon:
                self.icon = self.temp_icon.data
                self.icon_view.content.src = self.temp_icon.data
                self.icon_view.update()
        
        def close_dialog(e):
            on_dismiss(e)
            self.page.close(dialog)

        x_close = ft.Container(
            content= ft.Image(
                src= srcs.X_MARK,
                fit= ft.ImageFit.CONTAIN,
                width= self.height * 0.02,
                height= self.height * 0.02,
                color= 'red'
            ),
            on_click= close_dialog,
        )

        icon = controls[1].controls[0]
        dialog.content = ft.Container(
            alignment= ft.alignment.center,
            bgcolor= colors.FLET_DEFAULT,
            height= ((icon.height + (self.width * 0.01)) * 6),
            width= ((icon.width + (self.width * 0.01)) * 8),

            content= ft.Column(
                controls=[
                    ft.Row(
                        alignment= ft.MainAxisAlignment.END,
                        width= ((icon.width + (self.width * 0.01)) * 8),
                        controls= [x_close],
                    ),
                    ft.Column(
                        horizontal_alignment= ft.CrossAxisAlignment.END,
                        height= ((icon.height + (self.width * 0.01)) * 6),
                        spacing=self.width * 0.01,
                        scroll= ft.ScrollMode.ALWAYS,
                        controls=controls,
                    ),
                ],
            ),  
        )
        dialog.on_dismiss = on_dismiss

        self.page.open(dialog)
        pass

    def open_confirm(self, e):
        self.alerts.open_confirm(
            name= self.name,
            time= self.time,
            event= self.save_sched
        )
        pass

    def open_edit_confirm(self, e):
        self.alerts.open_edit_confirm(
            date= self.data['date'],
            time= self.data['time'],
            old_name= self.data['name'],
            event= self.edit_sched,
        )
        pass

    def open_remove_confirm(self, e):
        self.alerts.open_remove_confirm(
            name= self.name,
            event= self.remove_sched
        )
        pass

    def open_creation_success(self, e):
        self.page.overlay.clear()
        self.page.update()

        time.sleep(0.3)

        self.alerts.open_creation_success(
            name= self.name
        )
        pass

    def open_overwrite_confirm(self, scheds=None):
        time.sleep(0.3)

        self.alerts.open_overwrite_confirm(
            name= self.name,
            scheds= scheds,
            event= self.overwrite_sched
        )
        pass

    def _icon_btn_on_hover(self, e, color):
        if color == None:
            color = colors.BLACK_3
            self.icon_view.content.color = colors.WHITE_1 if self.icon_view.content.color == colors.CTHEME_1 else colors.CTHEME_1

        con = e.control
        con.bgcolor = colors.CTHEME_1 if con.bgcolor == color else color
        con.update()
        pass

    def _btns_on_hover(self, e, color):
        control = e.control
        control.bgcolor = colors.CTHEME_1 if control.bgcolor == color else color
        control.update()
        pass

    def _name_on_change(self, e):
        control = e.control
        self.name = control.value.strip()

    def _annotation_on_change(self, e):
        control = e.control
        self.annotation = control.value

    def _time_str(self):
        time = self.time
        hour = time.hour if time.hour > 9 else f'0{time.hour}'
        min = time.minute if time.minute > 9 else f'0{time.minute}'
        return f'{hour} : {min}'

    def _date_str(self):
        date = self.date
        week = isoweekday_str[date.isoweekday()]
        month = month_english[date.month]
        day = date.day if date.day > 9 else f'0{date.day}'
        return f'{week}., {month} {day}.'
    
    def _minute_str(self):
        min = self.duration
        return min if min > 9 else f'0{min}'

    def _update_recent_colors_pick(self):
        recent_colors_control = self.color_picker.content.controls[1].controls
        options = self.options
        priorities = self.priorities

        last_colors = []
        op_len = len(options)
        control_len = len(recent_colors_control)
        for n in range(op_len, op_len if op_len > control_len else 0, -1):
            if n != 1: #'ADD PRIORITY'
                name = options[n-1].key
                color = priorities[name]['color']
                last_colors.append(color)

        for i in range(len(last_colors)):
            if last_colors[i]: recent_colors_control[i].bgcolor = last_colors[i]

    def _icon_build(self, src):
        icon_width = self.height * 0.09
        icon_height = self.height * 0.09

        def on_hover(e):
            icon.bgcolor = colors.CTHEME_1 if icon.bgcolor == colors.CDEFAULT else colors.CDEFAULT
            icon.update()

        def on_click(e):
            control = e.control
            icon.bgcolor = colors.CTHEME_1
            icon.on_hover = None if icon.on_hover == on_hover else on_hover
            icon.update()

            if self.temp_icon == control:
                self.temp_icon = None
                return
            
            old_control = self.temp_icon

            if old_control:
                old_control.bgcolor = colors.CDEFAULT
                old_control.update()

            self.temp_icon = control
        
        icon = ft.Container(
            bgcolor= colors.CDEFAULT,
            border= ft.border.all(1, colors.BLACK_3),
            border_radius= ft.border_radius.all(5),
            width= icon_width,
            height= icon_height,
            alignment=ft.alignment.center,
            data= src,

            content= ft.Image(
                src= src,
                color= colors.WHITE_1,
                fit= ft.ImageFit.CONTAIN,
                width= icon_width * 0.60,
                height= icon_height * 0.60,
            ),
            on_hover= on_hover,
            on_click= on_click,
        )

        return icon

    def _date_field_build(self):
        group = self.__group()
        time = self.time_txt
        date = self.date_txt
        btn = self.datepicker

        group.controls[0].content.value = 'Date: '
        group.controls[1].alignment = ft.MainAxisAlignment.CENTER
        group.controls[1].spacing = 0
        group.controls[1].controls = [
            ft.Container(
                width= group.controls[1].width / 3,
                alignment= ft.alignment.center,
                content= time,
            ),
            ft.Container(
                width= group.controls[1].width / 3,
                alignment= ft.alignment.center,
                content= date,
            ),
            ft.Container(
                width= group.controls[1].width / 3,
                alignment= ft.alignment.center,
                content= btn,
            ),
        ]

        return group
     
    def _duration_field_build(self):
        group = self.__group()
        time = self.minute_txt
        btn = self.timerpicker

        group.controls[0].content.value = 'Duration: '
        group.controls[1].alignment = ft.MainAxisAlignment.CENTER
        group.controls[1].spacing = 0
        group.controls[1].controls = [
            ft.Row(
                width= group.controls[1].width / 3,
                alignment= ft.MainAxisAlignment.CENTER,
                controls= [
                    time,
                    ft.Text(
                        ' Minutes',
                        color= colors.WHITE_1,
                        size= fontsize.S4
                    ),
                ],
            ),
            ft.Container(
                width= group.controls[1].width / 3,
                alignment= ft.alignment.center,
            ),
            ft.Container(
                width= group.controls[1].width / 3,
                alignment= ft.alignment.center,
                content= btn,
            ),
        ]

        return group

    def _priority_field_build(self):
        group = self.__group()
        dropdown = self.dropdown
        color_picker = self.color_picker_icon
        btn = self.icon_view

        group.controls[0].content.value = 'Priority: '
        group.controls[1].alignment = ft.MainAxisAlignment.CENTER
        group.controls[1].spacing = 0
        group.controls[1].controls = [
            ft.Container(
                alignment= ft.alignment.center,
                expand= True,
                content= ft.Row(
                    controls= [
                        dropdown,
                        color_picker,
                    ]
                ),
            ),
            ft.Container(
                width= group.controls[1].width / 3,
                alignment= ft.alignment.center,
                content= btn
            )
        ]

        return group

    def _annotation_field_build(self):
        group = self.__group()

        group.controls[0].content.value = 'Annotation: '
        group.controls[1].controls = [self.annotation_input]

        return group

    def _color_picker_build(self):
        color_picker = ColorPicker(color= "#c8df6f")
        
        # slot
        _colors = [
            '#272a2f',
            '#272a2f',
            '#272a2f',
            '#272a2f',
            '#272a2f',
            '#272a2f',
            '#272a2f',
            '#272a2f',
        ]

        def on_click(e):
            color_picker.color = e.control.bgcolor
            color_picker.update()

        recent_colors = []
        space = 5
        size = (color_picker.width / len(_colors)) - (space * 2)
        for color in _colors:
            recent_colors.append(
                ft.Container(
                    border= ft.border.all(1, 'black'),
                    border_radius= ft.border_radius.all(2),
                    width= size,
                    height= size,
                    bgcolor= color,
                    margin= space,
                    on_click= on_click,
                )
            )
        
        return ft.Container(
            bgcolor= colors.FLET_DEFAULT,
            content= ft.Column(
                controls=[
                    color_picker,

                    ft.Row(
                        spacing= 0,
                        width= color_picker.width,
                        alignment= ft.MainAxisAlignment.CENTER,
                        vertical_alignment= ft.CrossAxisAlignment.CENTER,
                        controls=recent_colors,
                    ),
                ],
            ),

            height= self.height * 0.60,
            data = color_picker,
        )

    def __group(self):
        _title = ft.Container(
            alignment = ft.alignment.center_left, 
            padding= ft.padding.only(left=20),
            height= (dividers.APP_LAYOUT_HEIGHT * 0.50) * 0.06,
            content= ft.Text(
                'group > controls > 0 > content:',
                size= fontsize.S2,
                color= colors.WHITE_1,
            ),
        )
        _row = ft.Row(
            width=self.width * 0.80,
            height=(dividers.APP_LAYOUT_HEIGHT * 0.50) * 0.25,
            spacing=self.width * 0.02,
            controls=[
                ft.Text('group > controls > 1')
            ],
        )
        return ft.Column(
            spacing=(dividers.APP_LAYOUT_HEIGHT * 0.50) * 0.01,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            controls = [
                _title,
                _row,
            ],
        )
    
    def __add_priority(self, color):
        if color:
            self.icon_view.content.color = colors.WHITE_1
            self.icon_view.bgcolor = color
        else:
            self.icon_view.content.color = colors.CTHEME_1
            self.icon_view.bgcolor = colors.BLACK_3
        
    def __mode_creator(self):
        icon = self.back.content.controls[0]
        icon.src = srcs.ARROW_LEFT

        text = self.back.content.controls[1]
        text.value = 'Edit'

        def on_click(e):
            self.controller.on_back_action()
        
        self.back.on_click = on_click
        self.next.on_click = self.open_confirm
        pass
    
    def __mode_preview(self):
        icon = self.back.content.controls[0]
        icon.src = srcs.ARROW_LEFT

        text = self.back.content.controls[1]
        text.value = 'Back'

        def on_click(e):
            self.controller.on_back_action()
            
        self.back.on_click = on_click
        self.next.on_click = self.open_confirm
        pass

    def __mode_edit(self):
        icon = self.back.content.controls[0]
        icon.src = srcs.TRASH

        text = self.back.content.controls[1]
        text.value = 'Remove'

        old_sched_id = self.data
        old_name = self.name
        old_date = self.date
        old_time = self.time

        self.data = {
            'id' : old_sched_id,
            'name': old_name,
            'date': old_date,
            'time' : old_time,
        }

        self.back.on_click = self.open_remove_confirm
        self.next.on_click = self.open_edit_confirm

        pass

    def __get_data(self):
        icon = self.icon if self.icon else srcs.BAN
        duration = self.duration if self.duration and self.duration != 0 else 60

        date = self.date
        time = self.time
        priority = self.priority
        annotation = self.annotation

        name = self.name
        
        if name is None or name == "":
            self.name_input.hint_text = 'Must have a name.'
            self.name_input.hint_style = ft.TextStyle(color='red', size=fontsize.S1)
            self.name_input.border_color = 'red'
            return self.name_input.update()

        return SchedDTO(
            name= name,
            icon= icon,
            date= date,
            duration= duration,
            time= time,
            priority= priority,
            annotation= annotation
        )