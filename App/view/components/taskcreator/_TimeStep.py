import flet as ft
import datetime

from App.view.resources.utility import colors, srcs, fontsize
from App.view.resources.utility.dicts import isoweekday_str, month_english


class TimeStep(ft.Container):
    def __init__(self, taskcreator, page):
        super().__init__()
        self.taskcreator = taskcreator
        self.page = page
        self.visible = False

        self.calendar_field = None
        self.watch_field = None
        self.clock_field = None

        self.content = self._time_build()

    def step_reset(self):
        self._date_str()
        self._duration_str()
        self._time_str()

    def next_btn_update(self):
        if self.taskcreator.duration: self.taskcreator.next.disabled = False
        else: self.taskcreator.next.disabled = True
        self.taskcreator.next.update()

    def open_calendar(self, e):
        d_week = self.taskcreator.date.isoweekday()
        i_week = 0 - d_week
        e_week = 6 - d_week

        ini_week = self.taskcreator.date + datetime.timedelta(days= i_week)
        end_week = self.taskcreator.date + datetime.timedelta(days= e_week)

        def update_values(e):
            if self.taskcreator.date != datepicker.value:
                self.taskcreator.date = datepicker.value.date()
                self._date_str()
                self.calendar_field.update()
            pass

        datepicker = ft.DatePicker(
            first_date= ini_week,
            last_date= end_week,
            on_change= update_values,
            value= self.taskcreator.date
        )
        self.page.open(
            datepicker
        )

    def open_watch(self, e):
        def update_values(e):
            _value = int(cupertino_timer_picker.value / 60)
            if cupertino_timer_picker.value > 3540:
                _value = 60

            self.taskcreator.duration = _value if self.taskcreator.time.minute + _value <= 60 else 60 - self.taskcreator.time.minute
            self._duration_str()
            self._time_str()
            self.watch_field.update()
            self.clock_field.update()
            self.next_btn_update()

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
            if time_picker.value.minute + self.taskcreator.duration > 60:
                self.taskcreator.duration = 60 - time_picker.value.minute
                self._duration_str()
                self.watch_field.update()

            if time_picker.value != self.taskcreator.time:
                self.taskcreator.time = time_picker.value
                self._time_str()
                self.clock_field.update()
            
        time_picker = ft.TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick your time slot",
            value= self.taskcreator.time,
            on_change= update_values,
        )

        self.page.open(time_picker)
        pass
   
    def _date_str(self):
        date_str = ''

        if self.taskcreator.date:
            week_day = isoweekday_str[self.taskcreator.date.isoweekday()]
            month = month_english[self.taskcreator.date.month]
            day = self.taskcreator.date.day
            year = self.taskcreator.date.year
            date_str = f'{week_day}., {month} {day}, {year}.'

        control = self.calendar_field.controls[0]
        control.value = date_str
        pass 

    def _duration_str(self):
        duration_str = ''

        if self.taskcreator.duration:
            duration = self.taskcreator.duration if self.taskcreator.duration > 9 else f'0{self.taskcreator.duration}'
            duration_str = f'{duration} Minutes'
        
        control = self.watch_field.controls[0]
        control.value = duration_str
        pass

    def _time_str(self):
        time_str = ''

        if self.taskcreator.time:
            pre = datetime.datetime.combine(datetime.date.today(), self.taskcreator.time)
            pos = pre + datetime.timedelta(minutes= self.taskcreator.duration)

            pre_hour = pre.hour if pre.hour > 9 else f'0{pre.hour}'
            pre_minute = pre.minute if pre.minute > 9 else f'0{pre.minute}'
            pos_hour = pos.hour if pos.hour > 9 else f'0{pos.hour}'
            pos_minute = pos.minute if pos.minute > 9 else f'0{pos.minute}'

            time_str = f'{pre_hour}:{pre_minute}h - {pos_hour}:{pos_minute}h'

        control = self.clock_field.controls[0]
        control.value = time_str
        pass

    def _time_build(self):
        group = self.taskcreator._group()
        title = group.controls[0]
        row = group.controls[1]

        calendar_btn = self.taskcreator._icon2(src= srcs.CALENDAR_REGULAR)
        watch_btn = self.taskcreator._icon2(src= srcs.STOP_WATCH)
        clock_btn = self.taskcreator._icon2(src= srcs.CLOCK_REGULAR)

        calendar_btn.alignment = ft.MainAxisAlignment.END
        watch_btn.alignment = ft.MainAxisAlignment.END
        clock_btn.alignment = ft.MainAxisAlignment.END

        calendar_btn.controls[0].on_click = self.open_calendar
        watch_btn.controls[0].on_click = self.open_watch
        clock_btn.controls[0].on_click = self.open_clock
        
        calendar_field = ft.Row(
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
            alignment= ft.MainAxisAlignment.CENTER,
            spacing= self.taskcreator.width * 0.02,
            width= row.width / 3,
            height= row.height,
            controls=[
                ft.Text(
                '...',
                size=fontsize.S4,
                color=colors.WHITE_1,
                ),

                calendar_btn,
            ],
        )
        self.calendar_field = calendar_field

        watch_field = ft.Row(
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
            alignment= ft.MainAxisAlignment.CENTER,
            spacing= self.taskcreator.width * 0.02,
            width= row.width / 3,
            height= row.height,
            controls=[
                ft.Text(
                '... Minutes',
                size=fontsize.S4,
                color=colors.WHITE_1,
                ),

                watch_btn,
            ],
        )
        self.watch_field = watch_field

        clock_field = ft.Row(
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
            alignment= ft.MainAxisAlignment.CENTER,
            spacing= self.taskcreator.width * 0.02,
            width= row.width / 3,
            height= row.height,
            controls=[
                ft.Text(
                '00:00h - 00:00h',
                size=fontsize.S4,
                color=colors.WHITE_1,
                ),

                clock_btn,
            ],
        )
        self.clock_field = clock_field

        title.content.value = 'Time: '
        row.controls = [
            calendar_field,
            watch_field,
            clock_field,
        ]  
        return group