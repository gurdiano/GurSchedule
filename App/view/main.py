import flet as ft

from App.view.layout.headers import headers 
from App.view.layout.body import body 
from App.view.layout.footers import footers 

from App.view.model.headers.datepicker import datepicker
from App.view.model.body.markers import markers
from App.view.model.body.table import table, create

def main(page: ft.Page):
    page.title = "GurSchedule"
    page.padding = 0
                      
    page.window.width = 1356
    page.window.height = 678
    page.window.frameless = True
 
    widget = ft.Container(
        width=page.window.width,
        height=page.window.height,
        alignment=ft.alignment.center,
        # border=ft.border.all(2, 'white')
    )

    def tab_changer(e):
        _table.content = create(_table, _markers, _datepicker)
        _table.update()

    _datepicker = datepicker(widget, tab_changer)
    _markers = markers(widget)
    _table = table(widget, _markers, _datepicker)

    _headers = headers(widget, _datepicker)
    _body = body(widget, _markers, _table)
    _footers = footers(widget)

    widget.content = ft.Column(
        spacing=0,
        
        controls=[
            _headers,
            _body,
            _footers
        ]
    )
    
    page.add(
        ft.WindowDragArea(
            widget
        )
    )

ft.app(main)