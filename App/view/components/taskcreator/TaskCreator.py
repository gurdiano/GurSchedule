import flet as ft

from App.view.resources.utility import colors
from App.view.resources.utility import fontsize
from App.view.resources.utility import srcs

from ._Stepper import Stepper
from ._RecentStep import RecentStep
from ._TaskStep import TaskStep
from ._TimeStep import TimeStep
from ._PriorityStep import PriorityStep

from App.dtos.SchedDTO import SchedDTO

class TaskCreator(ft.Container):
    def __init__(self, controller, page):
        super().__init__()
        self.controller = controller
        self.page = page
        self.width = self.page.window.width * 0.50
        self.height = self.page.window.height * 0.50
        self._width = self.page.window.width * 0.50
        self._height = self.page.window.height * 0.50
        self.alignment = ft.alignment.top_center
        self.bgcolor = colors.BLACK_1
        self.border = ft.border.all(1, colors.BLACK_3)
        self.padding = ft.padding.only(top= self.width * 0.06, bottom= self.width * 0.06, left=self.width * 0.05, right=self.width * 0.05)

        self.icon = None
        self.name = None
        self.date = None
        self.duration = None
        self.time = None
        self.priority = None
        self.annotation = None

        self.header = ft.Container(
            width= self.width,
            height= self.height * 0.15,
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
                        width=self.height * 0.05,
                        height=self.height * 0.05,
                    ),
                ],
            ),
        )
        self.next = ft.CupertinoButton(
            bgcolor=colors.CTHEME_1,
            width=self.width * 0.20,
            height=self.height * 0.15,
            alignment=ft.alignment.center,
            content=ft.Row(
                spacing= self.width * 0.01,
                alignment= ft.MainAxisAlignment.CENTER,
                vertical_alignment= ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        'Next',
                        size=fontsize.S1,
                        color=colors.WHITE_1,
                    ),
                    ft.Image(
                        src=srcs.ARROW_RIGHT,
                        fit=ft.ImageFit.CONTAIN,
                        color=colors.WHITE_1,
                        width=self.height * 0.04,
                        height=self.height * 0.04,
                    ),
                ],
            ),
            on_click= self.next_step
        )
        self.back = ft.CupertinoButton(
            bgcolor=colors.CDEFAULT,
            width=self.width * 0.20,
            height=self.height * 0.15,
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
                        width=self.height * 0.04,
                        height=self.height * 0.04,
                    ),
                    ft.Text(
                        'Back',
                        size=fontsize.S1,
                        color=colors.BLACK_0,
                    ),
                ],
            ),
            visible=False,
            on_click=self.back_step,
        )
        
        self.stepper = Stepper(self.page, self)

        self.recent_content = RecentStep(self, page)
        self.task_content = TaskStep(self, page)
        self.time_content = TimeStep(self, page)
        self.priority_content = PriorityStep(self, page)

        self.content = ft.Column(
            width=self.width,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls= [
                self.header,

                ft.Container(
                    content= self.stepper,
                    alignment=ft.alignment.center,
                ),

                self.recent_content,
                self.task_content,
                self.time_content,
                self.priority_content,

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

        self.current = 0
        self.current_step = {
            0 : self.recent_content,
            1 : self.task_content,
            2 : self.time_content,
            3 : self.priority_content,
        }
        self.current_size = {
            0 : [self.page.window.width * 0.50, self.page.window.height * 0.50],
            1 : [self.page.window.width * 0.50, self.page.window.height * 0.80],
            2 : [self.page.window.width * 0.50, self.page.window.height * 0.60],
            3 : [self.page.window.width * 0.50, self.page.window.height * 0.80],
        }

    def completed(self):
        data = SchedDTO(
            icon= self.icon.content.src if self.icon else srcs.BAN,
            name= self.name,
            date= self.date,
            duration= self.duration,
            time= self.time,
            priority= self.priority,
            annotation= self.annotation,
        )

        self.controller.on_completed(data)
        pass

    def reset(self, date, time):
        self.date = date
        self.time = time
        self.duration = 60

        self.name = None
        self.priority = {'name': 'DEFULT', 'src': srcs.BAN, 'color': None}
        self.annotation = None

        size = self.current_size[0]
        self.width = size[0]
        self.height = size[1]
        
        self.recent_content.step_reset()
        self.task_content.step_reset()
        self.time_content.step_reset()
        self.priority_content.step_reset()

        self.current = 0
        self.task_content.visible = False
        self.time_content.visible = False
        self.priority_content.visible = False
        self.recent_content.visible = True
        pass

    def selected_task(self, sched_id):
        self.controller.on_selected_task(sched_id)
        pass

    def next_step(self, e):
        curr = self.current 
        nxt = self.current + 1 if self.current <= 2 else 0

        if curr == 3: return self.completed()
        self.__change_step(curr, nxt)
        self.__set_sizes(nxt)
        pass

    def back_step(self, e):
        curr = self.current 
        nxt = self.current - 1 
        self.__change_step(curr, nxt)
        self.__set_sizes(nxt)
        pass

    def _icon(self, color, src, name):
        _width = self._height * 0.15 
        _height = self._height * 0.15 
            
        _name = f'{name[:6]}...' if len(name) >= 8 else name
        _tooltip = name if len(name) >= 8 else None

        def _default_on_click(e):
            control = e.control
            data = control.parent.data
            self.selected_task(data)

        return ft.Column(
            spacing=0,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,

            controls=[
                ft.Container(
                    width= _width,
                    height= _height,
                    bgcolor= color,
                    border= ft.border.all(1, colors.BLACK_3),
                    border_radius= ft.border_radius.all(5),
                    alignment=ft.alignment.center,
                    on_click= _default_on_click,

                    content=ft.Image(
                        src=src,
                        fit=ft.ImageFit.CONTAIN,
                        width= _width * 0.60,
                        height= _height * 0.60,
                        color=colors.CTHEME_1 if color is None else colors.WHITE_1,
                    ), 
                ),

                ft.Text(
                    value = _name,
                    tooltip= _tooltip,
                    size=fontsize.S3,
                    color=colors.WHITE_1,
                    weight=ft.FontWeight.W_100,
                ),
            ],
        )

    def _icon2(self, src, name=None):
        _width = self._height * 0.15 
        _height = self._height * 0.15

        def _on_hover(e):
            control = e.control
            control.bgcolor = colors.CTHEME_1 if control.bgcolor == colors.CDEFAULT else colors.CDEFAULT
            control.update()

        def _on_click(e):
            if self.icon:
                self.icon.bgcolor = colors.CDEFAULT
                self.icon.on_hover = _on_hover
                self.icon.update()

            control = e.control
            control.bgcolor = colors.CTHEME_1
            control.on_hover = None
            control.update()
            self.icon = control

        return ft.Column(
            spacing=0,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,

            controls=[
                ft.Container(
                    width= _width,
                    height= _height,
                    bgcolor= colors.CDEFAULT,
                    border= ft.border.all(1, colors.BLACK_3),
                    border_radius= ft.border_radius.all(5),
                    alignment=ft.alignment.center,
                    data= src,
                    on_hover= _on_hover,
                    on_click= _on_click,

                    content=ft.Image(
                        src=src,
                        fit=ft.ImageFit.CONTAIN,
                        width= _width * 0.60,
                        height= _height * 0.60,
                        color=colors.WHITE_1,
                    ), 
                ),

                ft.Text(
                    name,
                    size=fontsize.S3,
                    color=colors.WHITE_1,
                    weight=ft.FontWeight.W_100,
                ),
            ],
        )

    def _group(self):
        _title = ft.Container(
            alignment = ft.alignment.center_left, 
            padding= ft.padding.only(left=20),
            height= self.height * 0.10,
            content= ft.Text(
                'group > controls > 0 > content:',
                size= fontsize.S2,
                color= colors.WHITE_1,
            ),
        )
        _row = ft.Row(
            width=self.width * 0.80,
            height=self.height * 0.25,
            spacing=self.width * 0.02,
            controls=[
                ft.Text('group > controls > 1')
            ],
        )
        return ft.Column(
            spacing=self.height * 0.02,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            controls = [
                _title,
                _row,
            ],
        )

    def __steps_update(self, step):
        if step == self.task_content:
            step_update = None
        if step == self.priority_content:
            self.priority_content.step_update()

    def __change_step(self, current, next):
        _curr_content = self.current_step[current]
        _nxt_content = self.current_step[next]

        _curr_content.visible = False if _curr_content.visible == True else True
        _nxt_content.visible = True if _nxt_content.visible == False else False
        self.back.visible = True if next !=0 else False
        self.stepper.visible = True if next !=0 else False

        _nxt_content.next_btn_update()

        _curr_content.update()
        _nxt_content.update()
        self.back.update()

        self.__steps_update(_nxt_content)
        self.stepper.next_step(next)
        self.current = next
        pass

    def __set_sizes(self, next_step):
        sizes = self.current_size[next_step]
        self.width = sizes[0]
        self.height = sizes[1]
        self.update()