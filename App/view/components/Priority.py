import flet as ft

from App.view.resources.utility import fontsize, colors, srcs


class Priority(ft.Container):
    def __init__(self, page, width=None, height=None, border_size=None, 
                border_raius=None, color=None, label_icon=None, label=None,
                text_size=None):
        super().__init__()
        self.page = page

        # self.bgcolor = 'red'

        self.menu_width = width if width else page.window.width * 0.30 
        self.menu_height = height if height else page.window.height * 0.10
        self.text_size = text_size

        self.label_icon = ft.Image(
            src= srcs.MAGNIFYING_GLASS,
            fit = ft.ImageFit.CONTAIN,
            color= color if color else colors.CDEFAULT,
            width= self.menu_height * 0.30,
            height= self.menu_height * 0.30,
        )
        self.label = ft.Text(
            label if label else 'Label value',
            size= text_size if text_size else 20, 
            color= color if color else colors.CDEFAULT,
        )

        self.down = ft.Container(
            content= ft.Image(
                src= srcs.CARET_DOWN,
                fit= ft.ImageFit.CONTAIN,
                color = color if color else colors.CDEFAULT,
                width= self.menu_height * 0.30,
                height= self.menu_height * 0.30,
            ),
            alignment= ft.alignment.center,
            width= self.menu_height * 0.50,
            height= self.menu_height * 0.50,
            border_radius= self.menu_height * 0.50,
            bgcolor= '#00000000',
            on_hover= self.drop_on_hover,
            on_click= self.drop_on_click,
        )
        self.up = ft.Container(
            content= ft.Image(
                src= srcs.CARET_UP,
                fit= ft.ImageFit.CONTAIN,
                color = color if color else colors.CDEFAULT,
                width= self.menu_height * 0.30,
                height= self.menu_height * 0.30,
            ),
            alignment= ft.alignment.center,
            width= self.menu_height * 0.50,
            height= self.menu_height * 0.50,
            border_radius= self.menu_height * 0.50,
            bgcolor= '#00000000',
            on_hover= self.drop_on_hover,
            on_click= self.drop_on_click,
        )

        self.field_0 = self._field_0(self.label_icon)
        self.field_1 = self._field_1(self.label)
        self.field_2 = self._field_2(self.down)

        self.menu = ft.Container(
            width = self.menu_width,
            height= self.menu_height,
            border_radius = border_raius if border_raius else ft.border_radius.all(3),
            border = ft.border.all(
                border_size if border_size else 2, 
                color if color else colors.CDEFAULT
            ),
            content= ft.Row(
                spacing= 0,
                controls= [
                    self.field_0,
                    self.field_1,
                    self.field_2,
                ],
            ),
        )

        self.options = ft.Column(
            spacing=0,
            visible= False,
            controls= [],
        )

        self.set_options()
        
        self.content = ft.Column(
            spacing=0,
            controls= [
                self.menu,
                self.options,
            ],
        )
        
    def drop_on_hover(self, e):
        control = e.control
        control.bgcolor = '#0DFFFFFF' if control.bgcolor == '#00000000' else '#00000000'
        control.update()

    def drop_on_click(self, e):
        control = e.control
        control.bgcolor = '#00000000' if control.bgcolor == '#0DFFFFFF' else '#0DFFFFFF'
        self.field_2.content = self.up if self.field_2.content == self.down else self.down
        self.field_2.update()

    def add_option(self, color=None, i_src=None, text=None,):
        icon = None
        label = None

        if i_src:
            icon = ft.Image(
                src= i_src,
                fit = ft.ImageFit.CONTAIN,
                color= color if color else colors.CDEFAULT,
                width= self.menu_height * 0.30,
                height= self.menu_height * 0.30,
            )
        if text:
            label = ft.Text(
                label if label else 'Label value',
                size= self.text_size if self.text_size else 20, 
                color= color if color else colors.CDEFAULT,
            )

        row = ft.Row(
            spacing= 0,
            controls= [
                self._field_0(icon),
                self._field_1(label),
                self._field_2(),
            ]
        )
        
        self.options.controls.append(row)

        return row

    def set_options(self):
        self.add_option(
            color=colors.WHITE_1,
            text= 'Critical',
            i_src= srcs.MOOM_SOLID,
        )
        self.add_option(
            color=colors.WHITE_1,
            text= 'Important',
            i_src= srcs.CART,
        )
        self.add_option(
            color=colors.WHITE_1,
            text= 'Regular',
            i_src= srcs.DUMBBELL,
        )
        
        self.options.visible = True

    def _field_0(self, content=None):
        return ft.Container(
            width= self.menu_width * 0.20,
            height= self.menu_height,
            alignment= ft.alignment.center,
            content= content,
        )

    def _field_1(self, content=None):
        return ft.Container(
            width= self.menu_width * 0.60,
            height= self.menu_height,
            alignment= ft.alignment.center_left,
            content= content,
        )
    
    def _field_2(self, content=None):
        return ft.Container(
            width= self.menu_width * 0.20,
            height= self.menu_height,
            alignment= ft.alignment.center,
            content= content,
        )


