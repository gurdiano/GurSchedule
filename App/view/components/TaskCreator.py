import flet as ft

class TaskCreator(ft.Container):
    def __init__(self, controller, page):
        super().__init__()
        self.controller = controller
        self.page = page

        self.width = self.page.window.width * 0.40
        self.height = self.page.window.height * 0.80
        self.alignment = ft.alignment.top_center
        self.bgcolor = '#0Dffffff'
        self.border = ft.border.all(2, 'white')
        self.padding = 5

        #day
        self.date = self.input_view('date', 'YYYY-MM-DD')
        #scheduler
        self.annotation = self.input_view('annotation')
        self.begin =  self.input_view('begin', 'HH:MM')
        #task
        self.name = self.input_view('name')
        self.duration = self.input_view('duration')
        #priority
        self.priority_name = self.input_view('priority name')
        self.priority_color = self.input_view('priority color')
        #icon
        self.icon = self.input_view('icon src')
    
    def create_sched(self, e):
        # self.controller.create_sched(date, src, p_name, p_color, p_icon, name, duration, begin, annotation)

        from App.view.resources.utility.srcs import MOOM_SOLID
        import datetime

        if self.date.value: yy, mm, dd = map(int, self.date.value.split('-'))
        if self.begin.value: hh, nn = map(int, self.begin.value.split(':'))

        date = None
        begin = None

        if self.date.value: date= datetime.date(yy, mm, dd)
        if self.begin.value: begin = datetime.time(hh, nn)

        src = self.icon.value
        p_name = self.priority_name.value
        p_color = self.priority_color.value
        p_icon = None
        name = self.name.value
        duration = self.duration.value
        annotation = self.annotation.value

        dd = self.controller.create_day(date)
        ii = self.controller.create_icon(src)
        pp = self.controller.create_priority(p_name, p_color, p_icon)
        tt = self.controller.create_task(name, duration, ii)
        ss = self.controller.create_sched(dd, pp, tt, begin, annotation)

    def input_view(self, label, hint=None):
        return ft.TextField(
            label=label,
            width=self.width * 0.70,
            hint_text=hint
        )

    def box(self, father, txt, content):
        text = ft.Text(
            txt,
            color= 'white',
            size= 12
        )

        contents = [text]
        for i in content:
            contents.append(i)

        return ft.Container(
            border=ft.border.all(1, 'white'),
            width=father.width * 0.80,
            # height=father.height * 0.40,
            alignment=ft.alignment.center,
            padding=5,
            content= ft.Column(
                spacing=20,
                controls=contents
            )
        )

    def build(self):
        next_btn = ft.ElevatedButton(
            text='Next',
            color='white',
            bgcolor='green',
            on_click=self.create_sched
        )

        discard_btn = ft.ElevatedButton(
            text='Discard',
            color='white',
            bgcolor='red'
        )

        rr = ft.Row(
            spacing=10,
            wrap=True,
            controls=[
                discard_btn,
                next_btn
            ],
        )

        self.content = ft.Column(
            width=self.width,
            height=self.height,
            spacing= 20,
            scroll= ft.ScrollMode.ALWAYS,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.box(self,  'Day', [self.date]),
                self.box(self, 'Task', [self.name]),
                self.box(self, 'Scheduler', [self.begin, self.annotation]),
                self.box(self, 'Priority', [self.priority_color, self.priority_name]),
                self.box(self, 'Icon', [self.icon]),
                rr,
            ],
        )
    

        