import flet as ft 

from App.view.component.Table import Table
from App.view.model.task import task_display
from .column import column
from .row import row

def create(father: ft.Container, markers, datepicker):
    columns = []
    for n in range(7):
        rows = []
        for j in range(24):
            r = row(father, markers, datepicker, j, n)
            _task = task_display(r)
            r.content = _task
            rows.append(r)
        
        c = column(father.father)
        c.content = ft.Column(
            spacing=0,
            controls=rows
        )
        columns.append(c)
    return ft.Row(
        spacing=0,

        controls=columns
    )
    
def table(father: ft.Container, markers, datepicker):
    tb = Table(father, markers, datepicker)
    tb.content = create(tb, markers, datepicker)

    return tb