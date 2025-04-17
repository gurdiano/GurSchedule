import flet as ft
from App.view.component.Task import Task
from App.view.service.SchedService import SchedService

from App.view.utility.fontsize import s3
from App.view.utility.colors import black_0, black_3, white_2, theme_1
from App.view.utility.convs import color_grad
from .task_view import task_view

def _icon(father, src, color):
    circle = ft.CircleAvatar(
        bgcolor=black_0,
        width=father.height * 0.60,
        height=father.height * 0.60,
    )

    border = ft.CircleAvatar(
        bgcolor=color,
        width=circle.height * 1.20,
        height=circle.height * 1.20,
        content=circle
    )

    svg = ft.Image(
        src=src,
        fit=ft.ImageFit.CONTAIN,
        width=circle.height * 0.80,
        height=circle.height * 0.80,
        color=color
    )

    circle.content = svg

    return border

def _text(title, color):
    return ft.Text(
        title.upper(),
        size=s3,
        color=color,
        weight=ft.FontWeight.W_600
    )

def _task_priority(row, title, i_src, color):
    icon = _icon(row, i_src, color)
    text = _text(title, white_2)

    gradient = ft.LinearGradient(
        begin = ft.alignment.center_right,
        end = ft.alignment.center_left,
        colors = color_grad(color),
    ) 

    task = Task(
        father=row,
        text=text,
        icon=icon,
        gradient=gradient,
    )

    task.border = ft.border.all(2, color)

    return task

def _task_default(row, title, i_src, color):
    icon = _icon(row, i_src, theme_1)
    text = _text(title, white_2)

    task = Task(
        father=row,
        text=text,
        icon=icon,
        color=color,
    )

    task.border = ft.border.all(2, black_3)
    
    return task

def _on_click(e):
    con = e.control
    page = con.page

    page.open(
        task_view(con)
    )

def task_display(row):
    date = row.data['date']
    time = row.data['time']
    
    scheds = SchedService.get_scheds(date, time)

    sched = scheds[0] if scheds else None #temp

    if sched:
        task = sched.task
        icon = task.icon
        priority = sched.priority

        title = task.name
        i_src = icon.src
        color = priority.color

        if color: container = _task_priority(row, title, i_src, color=color)
        else: container = _task_default(row, title, i_src, color=color)

        container.on_click = _on_click
        container.data = {
            'sched': sched
        }

        return container