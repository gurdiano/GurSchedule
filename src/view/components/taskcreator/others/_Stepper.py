import flet as ft

from view.resources.utility import colors
from view.resources.utility import fontsize
from view.resources.utility import srcs

class Stepper(ft.Column):
    def __init__(self, parent, page):
        super().__init__()

        self.page = page
        self.parent = parent
        self.width = parent.width * 0.50
        self.height = parent.height * 0.15
        self.data = 0

        self.spacing = 0
        self.alignment= ft.MainAxisAlignment.CENTER
        self.visible = False

        self.border_0 = self._border_circle()
        self.border_1 = self._border_circle()
        self.border_2 = self._border_circle()
        self.border_3 = self._border_circle()

        self.circle_0 = self._circle()
        self.circle_1 = self._circle()
        self.circle_2 = self._circle()
        self.circle_3 = self._circle()
        
        self.title0 = self._title()
        self.title1 = self._title()
        self.title2 = self._title()
        self.title3 = self._title()
        
        self.line_1 = self._line()
        self.line_2 = self._line()
        self.line_3 = self._line()

        self.borders = {
            0 : self.border_0,
            1 : self.border_1,
            2 : self.border_2,
            3 : self.border_3,
        }
        self.circles = {
            0 : self.circle_0,
            1 : self.circle_1,
            2 : self.circle_2,
            3 : self.circle_3,
        }
        self.titles = {
            0 : self.title0,
            1 : self.title1,
            2 : self.title2,
            3 : self.title3,
        }
        self.lines = {
            1 : self.line_1,
            2 : self.line_2,
            3 : self.line_3,
        }

    def next_step(self, step):
        step -= 1

        if step < 0: return self.__reset()
        if step == 0: self.__reset()
        if step > 0: self.__on_completed(step - 1)
        return self.__on_step(step)

    def _border_circle(self):
        return ft.CircleAvatar(
            width= self.width * 0.05,
            height= self.width * 0.05,
            bgcolor= colors.CDEFAULT,
        )
    
    def _circle(self):
        return ft.CircleAvatar(
            width= self.width * 0.04,
            height= self.width * 0.04,
            bgcolor= colors.BLACK_1,
        )
    
    def _check(self):
        return ft.Image(
            src= srcs.CHECK,
            fit=ft.ImageFit.CONTAIN,
            width= self.width * 0.03,
            height= self.width * 0.03,
            color= colors.CTHEME_1,
        )

    def _title(self):
        return ft.Text(
            'title',
            size=fontsize.S4,
            color=colors.CDEFAULT,
            width=self.width / 4,
            text_align= 'center',
        )
    
    def _line(self):
        return ft.Container(
            bgcolor= colors.CDEFAULT,
            width= self.width * 0.20,
            height= self.height * 0.04,
        )
    
    def __on_step(self, step):
        border = self.borders [step]
        circle = self.circles [step]
        title = self.titles [step]

        border.bgcolor = colors.CTHEME_1 
        circle.bgcolor = colors.CTHEME_1 
        title.color = colors.CTHEME_1 
        
        border.update()
        circle.update()
        title.update()

        if step < 3:
            nxt_line = self.lines[step + 1]
            nxt_border = self.borders[step + 1]
            nxt_circle = self.circles[step + 1]
            nxt_title = self.titles[step + 1]

            nxt_line.bgcolor = colors.CDEFAULT
            nxt_border.bgcolor = colors.CDEFAULT
            nxt_circle.bgcolor = colors.BLACK_1
            nxt_circle.content = None
            nxt_title.color = colors.CDEFAULT

            nxt_line.update()
            nxt_border.update()
            nxt_circle.update()
            nxt_title.update()
        pass

    def __on_completed(self, step):
        border = self.borders [step]
        circle = self.circles [step]
        title = self.titles [step]
        

        border.bgcolor = colors.CTHEME_1
        circle.bgcolor = colors.BLACK_1
        circle.content = self._check()
        title.color = colors.CTHEME_1

        if step <  3:
            line = self.lines [step + 1]
            line.bgcolor = colors.CTHEME_1
            line.update()

        border.update()
        circle.update()
        title.update()
        
        pass

    def __reset(self):
        self.border_0.bgcolor = colors.CDEFAULT
        self.circle_0.bgcolor = colors.BLACK_1
        self.circle_0.content = None
        self.title0.color = colors.CDEFAULT

        self.line_1.bgcolor = colors.CDEFAULT
        self.border_1.bgcolor = colors.CDEFAULT
        self.circle_1.bgcolor = colors.BLACK_1
        self.circle_1.content = None
        self.title1.color = colors.CDEFAULT
        
        self.line_2.bgcolor = colors.CDEFAULT
        self.border_2.bgcolor = colors.CDEFAULT
        self.circle_2.bgcolor = colors.BLACK_1
        self.circle_2.content = None
        self.title2.color = colors.CDEFAULT
        
        self.line_3.bgcolor = colors.CDEFAULT
        self.border_3.bgcolor = colors.CDEFAULT
        self.circle_3.bgcolor = colors.BLACK_1
        self.circle_3.content = None
        self.title3.color = colors.CDEFAULT

        self.border_0.update()
        self.circle_0.update()
        self.title0.update()
        self.line_1.update()
        self.border_1.update()
        self.circle_1.update()
        self.title1.update()
        self.line_2.update()
        self.border_2.update()
        self.circle_2.update()
        self.title2.update()
        self.line_3.update()
        self.border_3.update()
        self.circle_3.update()
        self.title3.update()
        pass

    def build(self):
        self.border_0.content = self.circle_0
        self.border_1.content = self.circle_1
        self.border_2.content = self.circle_2
        self.border_3.content = self.circle_3

        self.title0.value = 'Task'
        self.title1.value = 'Time'
        self.title2.value = 'Priority'
        self.title3.value = 'Completed'

        row1 = ft.Row(
            spacing=0,
            alignment= ft.MainAxisAlignment.CENTER,
            controls = [
                self.border_0,
                self.line_1,
                self.border_1,
                self.line_2,
                self.border_2,
                self.line_3,
                self.border_3,
            ],
        )
        row2 = ft.Row(
            spacing=0,
            controls=[
                self.title0,
                self.title1,
                self.title2,
                self.title3,
            ],
        )
        self.controls = [
            row1,
            row2,
        ]