import flet as ft

class TaskDetails(ft.AlertDialog):
    def __init__(self, controller, page, date, name, icon_src, duration, begin, priority, color, annotation):
        super().__init__()
        self.controller = controller
        self.page = page
        self.bgcolor = '#00000000'

        self.date = date
        self.name = name
        self.icon_src = icon_src
        self.duration = duration
        self.begin = begin
        self.priority = priority
        self.color = color
        self.annotation = annotation

        self.container = ft.Container(
            width=page.height * 0.50,
            height=page.height * 0.50,
            bgcolor='white'
        )

        self.head = ft.Container(
            width=self.container.width,
            height=self.container.height * 0.20,
            border=ft.border.all(2, 'black'),
            alignment=ft.alignment.center,

            content=ft.Text(
                'Task',
                size=12,
                color='black'
            )
        )

        self.body = ft.Container(
            width=self.container.width,
            height=self.container.height * 0.80,
            border=ft.border.all(2, 'black'),
            alignment=ft.alignment.center,

            content= ft.Column(
                controls=[
                    ft.Text(f'dia: {self.date}', size=10, color='black'),
                    ft.Text(f'name: {self.name}', size=10, color='black'),
                    ft.Text(f'icone: {self.icon_src}', size=10, color='black'),
                    ft.Text(f'duração: {self.duration}minutos', size=10, color='black'),
                    ft.Text(f'Início: {self.begin}', size=10, color='black'),
                    ft.Text(f'Prioridade: {self.name} - {self.color}', size=10, color='black'),
                    ft.Text(f'Anotação: {self.annotation}', size=10, color='black'),
                ]
            )
        )

    def build(self):
        self.container.content = ft.Column(
            spacing=0,
            controls=[
                self.head,
                self.body
            ]
        )

        self.content = self.container