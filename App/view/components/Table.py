import flet as ft
import datetime

from App.view.resources.utility.dicts import isoweek_day
from App.view.resources.utility.dividers import ROW5, COL2
from App.view.resources.utility.colors import BLACK_0, BLACK_1, BLACK_2

class Table(ft.Row):
    def __init__(self, controller, page):
        super().__init__()
        self.controller = controller
        self.page = page
        self.width = page.window.width * 0.92
        self.height = page.window.height * 0.87
        self.spacing = 0
        self.general_date = datetime.date.today()
        self.columns = None
        self.rows = None
        self.create()
        self.load()

    def calculate_cell_date(self, date, column):
        iso = date.isoweekday()
        weekday = isoweek_day[iso]
        res = column - weekday 
        return date + datetime.timedelta(days=res)
    
    def _on_hover(self, e, row):
        con = e.control
        con.bgcolor = BLACK_2 if con.bgcolor == BLACK_1 else BLACK_1
        
        self.page.pubsub.send_all_on_topic(f'markers/{row}', e)
        self.page.pubsub.send_all_on_topic(f'picker', con.data['date'])

        con.update()
    
    def row(self, row, col):
        col = col + 1
        date = self.calculate_cell_date(self.general_date, col)
        return ft.Container(
            width=self.width,
            height=self.height * ROW5,
            bgcolor=BLACK_1,
            border=ft.border.all(1, BLACK_0),
            on_hover=lambda e: self._on_hover(e, row),
            data={
                'row': row, 
                'column': col, 
                'date': date,
                'time': datetime.time(row, 0)
            }  
        )
    
    def column(self, n):
        return ft.Container(
            width=self.page.window.width * COL2,
            height=self.height,
            bgcolor=BLACK_0,
            data=n,
        )
    
    def load(self):
        for row in self.rows:
            date = row.data['date']
            hour = row.data['time'].hour
            row.content = self.controller.search_sched(date, hour)

    def rows_date_update(self, date):
        for row in self.rows:
            column = row.data['column']
            row.data['date'] = self.calculate_cell_date(date, column)
        self.load()
        self.update()
        
    def not_update(self):
        self.update()

    def create(self):
        all_rows = []

        columns = []
        for cc in range(7):
            column = self.column(cc)

            rows = []
            for rr in range(24):

                row = self.row(rr, cc)
                rows.append(row)
                all_rows.append(row)
            
            column.content = ft.Column(
                spacing=0,
                controls=rows
            )
            columns.append(column)

        self.columns = columns
        self.rows = all_rows
        self.controls = columns
        
        

            


                
            


    