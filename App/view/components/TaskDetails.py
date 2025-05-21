import flet as ft
import datetime

from App.view.resources.utility import colors, srcs, fontsize
from App.view.resources.utility.dicts import isoweekday_str, month_english

from App.dtos.SchedDTO import SchedDTO

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

        self.bgcolor = colors.BLACK_1
        self.width = self.page.window.width * 0.50
        self.height = self.page.window.height * 0.90
        self.border = ft.border.all(1, colors.BLACK_3)
        self.padding = ft.padding.only(
            top= self.width * 0.06, 
            bottom= self.width * 0.06, 
            left=self.width * 0.05, 
            right=self.width * 0.05
        )

        self.name_input = ft.TextField(
            # border= ft.InputBorder.UNDERLINE,
            border_color= colors.WHITE_1,
            width= self.width * 0.20,
            height= (self.page.window.height * 0.50) * 0.10,
            text_size= fontsize.S1,
            text_align= ft.TextAlign.CENTER,
            text_style= ft.TextStyle(color= colors.CTHEME_1),
            # content_padding= 0,
            on_change= self._name_on_change,
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
        self.colorpicker = ft.Container(
            border= ft.border.all(2, colors.WHITE_1),
            width= (self.page.window.height * 0.50) * 0.13,
            height= (self.page.window.height * 0.50) * 0.13,
            alignment= ft.alignment.center,
            bgcolor= None,
        )
        self.datepicker = ft.Container(
            bgcolor= colors.BLACK_0,
            width= self.width * 0.25,
            border= ft.border.all(1, colors.CDEFAULT),
            border_radius= ft.border_radius.all(3),
            alignment= ft.alignment.center,
            content= ft.Image(
                src= srcs.CALENDAR_REGULAR,
                fit= ft.ImageFit.CONTAIN,
                color= colors.WHITE_1,
                width= self.width * 0.05,
                height= self.width * 0.05,
            ),
            on_click= self.open_calendar,
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
            height= (self.page.window.height * 0.50) * 0.05,
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
                        width=(self.page.window.height * 0.50) * 0.05,
                        height=(self.page.window.height * 0.50) * 0.05,
                    ),
                ],
            ),
        )
        self.next = ft.CupertinoButton(
            bgcolor=colors.CTHEME_1,
            width=self.width * 0.20,
            height=(self.page.window.height * 0.50) * 0.15,
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
                        width=(self.page.window.height * 0.50) * 0.04,
                        height=(self.page.window.height * 0.50)* 0.04,
                    ),
                ],
            ),
            on_click= self.save_sched
        )
        self.back = ft.CupertinoButton(
            bgcolor=colors.CDEFAULT,
            width=self.width * 0.20,
            height=(self.page.window.height * 0.50) * 0.15,
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
                        width=(self.page.window.height * 0.50) * 0.04,
                        height=(self.page.window.height * 0.50) * 0.04,
                    ),
                    ft.Text(
                        'Edit',
                        size=fontsize.S1,
                        color=colors.BLACK_0,
                    ),
                ],
            ),
            visible=True,
            # on_click=self.back_step,
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

    def save_sched(self, e):
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

            schedDTO = SchedDTO(
                name= name,
                icon= icon,
                date= date,
                duration= duration,
                time= time,
                priority= priority,
                annotation= annotation
            )
            self.controller.on_save_sched(schedDTO)
            pass

    def update_view(self, u=None):
        self.name_input.value = self.name
        self.time_txt.value = self._time_str()
        self.date_txt.value = self._date_str()
        self.minute_txt.value = self._minute_str()
        self.dropdown.value = self.priority['name']
        self.icon_view.content.src = self.icon
        self.__add_priority(self.priority['color'])
        self.colorpicker.bgcolor = self.priority['color']
        self.annotation_input.value = self.annotation
        if u:
            self.name_input.update()
            self.time_txt.update()
            self.date_txt.update()
            self.minute_txt.update()
            self.dropdown.update()
            self.icon_view.update()
            self.colorpicker.update()
            self.annotation_input.update()

    def back_action(self, action):
        action = action.lower()

        if action == 'edit':
            text = self.back.content.controls[1]
            text.value = 'Edit'

            def on_click(e):
                self.controller.on_back_action()
            self.back.on_click = on_click
        
        if action == 'back_taskcreator':
            text = self.back.content.controls[1]
            text.value = 'Back'

            def on_click(e):
                self.controller.on_back_action()
            self.back.on_click = on_click
        
        if action == 'back_scheduler':
            text = self.back.content.controls[1]
            text.value = 'Back'

            def on_click(e):
                self.page.overlay.clear()
                self.page.update()
            self.back.on_click = on_click

    def update_priority(self, e):
            priority = self.priorities[e.data]
            color = priority['color']

            self.__add_priority(color)

            self.colorpicker.bgcolor = color
            self.priority = priority
            self.icon_view.update()
            self.colorpicker.update()

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
            if cupertino_timer_picker.value != 3540:
                self.duration = int(cupertino_timer_picker.value / 60)
                self.minute_txt.value = self._minute_str()
                self.minute_txt.update()

        cupertino_timer_picker = ft.CupertinoTimerPicker(
            value=3540,
            second_interval=10,
            minute_interval=1,
            mode=ft.CupertinoTimerPickerMode.HOUR_MINUTE,
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
        color_picker = self.colorpicker
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

    def __group(self):
        _title = ft.Container(
            alignment = ft.alignment.center_left, 
            padding= ft.padding.only(left=20),
            height= (self.page.window.height * 0.50) * 0.06,
            content= ft.Text(
                'group > controls > 0 > content:',
                size= fontsize.S2,
                color= colors.WHITE_1,
            ),
        )
        _row = ft.Row(
            width=self.width * 0.80,
            height=(self.page.window.height * 0.50) * 0.25,
            spacing=self.width * 0.02,
            controls=[
                ft.Text('group > controls > 1')
            ],
        )
        return ft.Column(
            spacing=(self.page.window.height * 0.50) * 0.01,
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