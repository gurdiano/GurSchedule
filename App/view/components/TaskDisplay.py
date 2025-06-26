import flet as ft
import bisect

from App.view.resources.utility.convs import color_grad

from App.view.resources.utility import srcs
from App.view.resources.utility import dividers
from App.view.resources.utility import colors
from App.view.resources.utility import fontsize 

class TaskDisplay(ft.Container):
    def __init__(self, controller, page, title, i_src, color, data):
        super().__init__()
        self.page = page
        self.controller = controller
        
        self.width = dividers.TABLE_WIDTH * dividers.COL2
        self.height = dividers.TABLE_HEIGHT * dividers.ROW5
        
        self.title = title
        self.i_src = i_src
        self.color = color
        self.data = data
        self.on_click = self._on_click

        self.more_tasks_control = []
        self.tasks = []
        self.times = {}
        # self.dialog = None
        # self.parent_control = None

        self.content = ft.Row(
            spacing=5,
            alignment= ft.MainAxisAlignment.START
        )
       
    def create_priority_view(self):
        icon = self._create_icon(self.i_src, self.color)
        text = self._create_text(self.title, colors.WHITE_2)

        gradient = ft.LinearGradient(
            begin = ft.alignment.center_right,
            end = ft.alignment.center_left,
            colors = color_grad(self.color),
        )
        self.gradient = gradient
        self.border = ft.border.all(2, self.color)
        return [icon, text]
    
    def create_default_view(self):
        icon = self._create_icon(self.i_src, colors.CTHEME_1)
        text = self._create_text(self.title, colors.WHITE_2)
        self.border = ft.border.all(2, colors.BLACK_3)
        self.bgcolor = self.color
        return [icon, text]

    def multitask_on_click(self, e):
        self.controller.multitask_on_click(self)
        pass
    
    def new_sched(self, e, dialog, parent):
        self.page.close(dialog)
        self.controller.on_new_sched(self, parent)
        pass

    def selected_display(self, e, parent, sched_id, dialog):
        self.controller.on_selected_display(parent, sched_id, dialog)
        pass

    def set_selected_on_click(self, parent, sched_id, dialog):
        self.on_click = lambda e: self.selected_display(e, parent, sched_id, dialog)
        pass

    def open_tasks(self, controls, dialog):
        width = self.width * 1.40
        height = self.height * 4
        
        rows_map = {}
        ord_time = []
        for control in controls:
            time = self.times[control.data]
            hour = time.hour if time.hour > 9 else f'0{time.hour}'
            minute = time.minute if time.minute > 9 else f'0{time.minute}'

            time_str = f' {hour}: {minute} '

            hour_display = ft.Container(
                width= self.width * 0.40,
                height= self.height,
                bgcolor= colors.BLACK_0,
                border= ft.border.all(1, colors.BLACK_3),
                alignment= ft.alignment.center,

                content= ft.Text(
                    value= time_str,
                    color= colors.CTHEME_1,
                    size= fontsize.S1,
                ),
            )
            row = ft.Row(
                spacing=0,
                controls=[
                    hour_display,
                    control,
                ],
            )
            bisect.insort(ord_time, time)
            rows_map[time] = row

        rows = []
        for time in ord_time:
            rows.append(
                rows_map[time]                
            )

        def on_hover(e):
            e.control.bgcolor = colors.CTHEME_1 if e.control.bgcolor == colors.CDEFAULT else colors.CDEFAULT
            e.control.update()

        _parent = self.parent
        add_btn = ft.Container(
            bgcolor= colors.CDEFAULT,
            border= ft.border.all(2, colors.CDEFAULT),
            width= width,
            height= self.height,
            alignment= ft.alignment.center,
            content= ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment= ft.CrossAxisAlignment.CENTER,

                controls = [
                    ft.Image(
                        src= srcs.PLUS,
                        fit= ft.ImageFit.CONTAIN,
                        height= self.height * 0.50,
                        width= self.height * 0.50,
                        color= colors.WHITE_2,
                    ),
                    ft.Text(
                        value= 'NEW',
                        color= colors.WHITE_2,
                        size= fontsize.S3,
                    ),
                ],
            ),

            on_hover= on_hover,
            on_click= lambda e: self.new_sched(e, dialog, _parent),
        )
        rows.append(add_btn)

        dialog.bgcolor = '#00000000'
        dialog.content = ft.Container(
            bgcolor= colors.BLACK_1,
            border= ft.border.all(1, colors.BLACK_3),
            border_radius= ft.border_radius.all(5),
            width= width,
            height= height,
            alignment=ft.alignment.center,
            
            content= ft.Column(
                spacing= 0,
                controls= rows,
                scroll= ft.ScrollMode.ALWAYS,
            ),
        )
        self.page.open(dialog)
        pass

    def add_more_task(self, sched_id, color, icon_src, time):
        color = color if color else colors.CTHEME_1

        if len(self.more_tasks_control) < 3:
            plus_icon = self._create_icon(color= color, src= icon_src)
            self.more_tasks_control.append(plus_icon)

        self.tasks.append(sched_id)
        self.times[sched_id] = time
        self.on_click = self.multitask_on_click
        pass

    def build(self):
        controls = self.create_priority_view() if self.color else self.create_default_view()

        main_content = ft.Row(
            spacing= 5,
            controls= controls,
            width= self.width * 0.60,
        )
        plus_content = ft.Row(
            spacing= 5,
            controls= self.more_tasks_control,
            alignment= ft.MainAxisAlignment.END,
            width= self.width * 0.40,
        )

        self.content.controls.append(main_content)
        self.content.controls.append(plus_content)
        pass

    def _on_click(self, e):
        self.controller.display_on_click(self)
        pass

    def _create_text(self, title, color):
        name = title if len(title) <= 10 else f'{title[:10]}...'

        return ft.Text(
            name.upper(),
            size=fontsize.S3,
            color=color,
            weight=ft.FontWeight.W_600,
            tooltip= title if len(title) > 10 else None
        )
    
    def _create_icon(self, src, color):
        circle = ft.CircleAvatar(
            bgcolor=colors.BLACK_0,
            width=self.height * 0.60,
            height=self.height * 0.60,
        )
        svg = ft.Image(
            src=src,
            fit=ft.ImageFit.CONTAIN,
            width=circle.height * 0.80,
            height=circle.height * 0.80,
            color=color
        )
        border = ft.CircleAvatar(
            bgcolor=color,
            width=circle.height * 1.20,
            height=circle.height * 1.20,
            content=circle
        )
        circle.content = svg
        return border