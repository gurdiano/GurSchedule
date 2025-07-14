import flet as ft

from view.resources.utility import colors, srcs

class RecentStep(ft.Container):
    def __init__(self, taskcreator, page):
        super().__init__()
        self.taskcreator = taskcreator
        self.page = page

        self.content = self._recent_build()

    def step_reset(self):
        self.taskcreator.stepper.visible = False
        self.taskcreator.next.disabled = False
        self.taskcreator.back.visible = False
        self.content = self._recent_build()

    def next_btn_update(self):
        self.taskcreator.next.disabled = False
        self.taskcreator.next.update()

    def more_btn(self):
        more_btn = self.taskcreator._icon(
            color=colors.BLACK_2,
            name='...',
            src=srcs.CHEVRON_RIGHT,
        )
        more_btn.controls[0].on_click = self.more_tasks
        return more_btn

    def load_icons(self, n, id):
        items = self.taskcreator.controller._load_scheds(n, id)
        
        icons = []
        for res in items:
            icon = self.taskcreator._icon(
                name= res['name'],
                src= res['src'],
                color= res['color'],
            )

            icon.data = res['id']
            icons.append(icon)
        return icons
    
    def more_tasks(self, e):
        control = self.content.controls[1]
        load_btn = control.controls.pop()
        
        last_task = control.controls[-1]
        remain = last_task.data - 8 

        if remain > 0:
            new_tasks = self.load_icons(8, last_task.data)
            new_tasks.append(load_btn)
        else:
            new_tasks = self.load_icons(8 + remain, last_task.data)

        control.controls.extend(new_tasks)
        control.update()
        pass
    
    def _recent_build(self):
        group = self.taskcreator._group()
        title = group.controls[0]
        row = group.controls[1]

        _controls = self.load_icons(9, None)

        if len(_controls) == 9: 
            _controls.pop()
            _controls.pop()
            _controls.append(self.more_btn())
        
        title.content.value = 'Recent tasks:'
        row.controls = _controls
        row.scroll = ft.ScrollMode.ALWAYS
        group.visible = True

        return group