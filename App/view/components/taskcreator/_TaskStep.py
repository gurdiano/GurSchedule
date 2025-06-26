import flet as ft

from .others._MoreIcons import MoreIcons

from App.view.resources.utility import colors, srcs, fontsize

class TaskStep(ft.Container):
    def __init__(self, taskcreator, page):
        super().__init__()
        self.taskcreator = taskcreator
        self.page = page
        self.visible = False

        self.content = self._task_build()

    def creat_icon(self, icon_src):
        return self.taskcreator.controller.on_creat_icon(icon_src)

    def step_reset(self):
        text_field = self.content.controls[1].controls[1].controls[0]
        text_field.value = self.taskcreator.name   

        if self.taskcreator.icon: 
            self.taskcreator.icon.bgcolor = colors.CDEFAULT
            self.taskcreator.icon = None

    def next_btn_update(self):
        if self.taskcreator.name: self.taskcreator.next.disabled = False
        else: self.taskcreator.next.disabled = True
        self.taskcreator.next.update()

    def load_icons2(self, n):
        items = self.taskcreator.controller._load_icons(n)

        icons = []
        for item in items:
            icon = self.taskcreator._icon2(item)
            icon.data = item
            icons.append(icon)
        
        return icons

    def more_icons(self, e):
        control = self.content.controls[0]
        row = control.controls[1]
        icons = self.load_icons2(None)
        
        _controls = []
        for n in range(0, len(icons), 8):
            _row = ft.Row(
                width=self.taskcreator._width * 0.80,
                spacing=self.taskcreator._width * 0.02,
            )
            for i in range(n, n + 8, 1):
                _row.controls.append(
                    icons[i]
                )
                if i + 1 == len(icons): break
            _controls.append(_row)

        moreIcons = MoreIcons(
            parent= self, 
            page= self.page,
            row=row, 
            all_icons=_controls
        )
        
        moreIcons.build()
        control.update()
        pass

    def _task_build(self):
        more_btn = self.taskcreator._icon(
            name= 'More',
            color= colors.BLACK_2,
            src= srcs.PLUS,
        )
        more_btn.controls[0].on_click = self.more_icons

        group = self.taskcreator._group()
        group2 = self.taskcreator._group()
        
        icons = self.load_icons2(7)
        icons.append(more_btn)

        group.controls[0].content.value = 'Icon: '
        group.controls[1].controls = icons

        def on_change(e):
            control = e.control
            self.taskcreator.name = control.value.strip()
            self.next_btn_update()
        

        group2.controls[0].content.value = 'Name: '
        group2.controls[1].controls = [ft.TextField(
            label= 'Name',
            border_color= colors.WHITE_1,
            border_width= 2,
            width= self.taskcreator.width * 0.40,
            height=self.taskcreator.height * 0.12,
            value= self.taskcreator.name,
            capitalization= ft.TextCapitalization.SENTENCES,
            on_change= on_change,
        )]
        group2.controls[1].vertical_alignment = ft.CrossAxisAlignment.START
        
        return ft.Column(
            spacing=0,
            controls=[
                group,
                group2,
            ],
        )
