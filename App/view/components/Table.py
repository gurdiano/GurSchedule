import flet as ft
import datetime

from App.view.resources.utility.dicts import isoweek_day
from App.view.resources.utility.dividers import ROW5, COL2
from App.view.resources.utility.colors import BLACK_0, BLACK_1, BLACK_2

from App.dtos.RowDTO import RowDTO

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
        self.rows_map = None
        self.create() # build()

    def load_scheds(self, date=None):
        if date:
            rows_map = {}
            for row in self.rows:
                row.content = None
                row.update()
                
                column = row.data['column']
                hour = row.data['row']
                new_date = self.__calculate_cell_date(date, column)
                name = self.get_row_name(new_date, hour)

                row.data['date'] = new_date
                rows_map[name] = row
            self.rows_map = rows_map

        first_date = self.rows[0].data['date']
        last_date = self.rows[-1].data['date']

        self.controller.on_load_scheds(first_date, last_date)
        pass

    def on_click(self, e):
        control = e.control
        data = control.data
        
        rowDTO = RowDTO(
            n_row= data['row'],
            n_column= data['column'],
            date= data['date'],
            time= data['time'],
            control= control
        )
        self.controller.row_on_click(rowDTO)
        pass

    def create(self):
        all_rows = []

        columns = []
        rows_map = {}
        for cc in range(7):
            column = self._column(cc)

            rows = []
            for rr in range(24):
                row = self._row(rr, cc)
                hour = row.data['row']
                date = row.data['date']
                rows_map[self.get_row_name(date, hour)] = row
                rows.append(row)
                all_rows.append(row)
            
            column.content = ft.Column(
                spacing=0,
                controls=rows
            )
            columns.append(column)

        self.columns = columns
        self.rows = all_rows
        self.rows_map = rows_map
        self.controls = columns
    
    def highlight_marker(self, e, row, date):
        self.controller.on_highlight_marker(e, row, date)

    def get_row_name(self, date, hour):
        return f'{date}-{hour}'

    def _on_hover(self, e, row):
        con = e.control
        con.bgcolor = BLACK_2 if con.bgcolor == BLACK_1 else BLACK_1
        date = con.data['date']
        con.update()
        
        self.highlight_marker(e, row, date)
        pass

    def _row(self, row, col):
        col = col + 1
        date = self.__calculate_cell_date(self.general_date, col)
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
            },
            on_click= self.on_click, 
        )
    
    def _column(self, n):
        return ft.Container(
            width=self.page.window.width * COL2,
            height=self.height,
            bgcolor=BLACK_0,
            data=n,
        )

    def __calculate_cell_date(self, date, column):
        iso = date.isoweekday()
        weekday = isoweek_day[iso]
        res = column - weekday 
        return date + datetime.timedelta(days=res)