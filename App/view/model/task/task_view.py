import flet as ft

def task_view(father):
    page = father.page
    sched = father.data['sched']

    container = ft.Container(
        width=page.height * 0.50,
        height=page.height * 0.50,
        bgcolor='white'
    )
    head = ft.Container(
        width=container.width,
        height=container.height * 0.20,
        border=ft.border.all(2, 'black'),
        alignment=ft.alignment.center,

        content=ft.Text(
            'Task',
            size=12,
            color='black'
        )
    )
    body = ft.Container(
        width=container.width,
        height=container.height * 0.80,
        border=ft.border.all(2, 'black'),
        alignment=ft.alignment.center,

        content= ft.Column(
            controls=[
                ft.Text(f'dia: {sched.day.date}', size=10, color='black'),
                ft.Text(f'name: {sched.task.name}', size=10, color='black'),
                ft.Text(f'icone: {sched.task.icon.src}', size=10, color='black'),
                ft.Text(f'duração: {sched.task.duration}minutos', size=10, color='black'),
                ft.Text(f'Início: {sched.begin}', size=10, color='black'),
                ft.Text(f'Prioridade: {sched.priority.name} - {sched.priority.color}', size=10, color='black'),
                ft.Text(f'Anotação: {sched.annotation}', size=10, color='black'),
            ]
        )
    )

    container.content = ft.Column(
        spacing=0,
        controls=[
            head,
            body
        ]
    )

    return ft.AlertDialog(
        bgcolor='#00000000',
        content=container
    )