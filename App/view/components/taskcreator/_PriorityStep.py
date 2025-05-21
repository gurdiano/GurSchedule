import flet as ft

from App.view.resources.utility import colors, srcs, fontsize

class PriorityStep(ft.Container):
    def __init__(self, taskcreator, page):
        super().__init__()
        self.taskcreator = taskcreator
        self.page = page
        self.visible = False

        self.priorities = None
        self.options = None
        self.priority_icon = None
        self.priority_picker = None

        self.icon = ft.Container(
            border= ft.border.all(2, colors.WHITE_1),
            width= self.taskcreator.height * 0.14,
            height= self.taskcreator.height * 0.14,
            border_radius= ft.border_radius.all(3),
            alignment= ft.alignment.center,
            content= ft.Image(
                src= srcs.BAN,
                fit= ft.ImageFit.CONTAIN,
                color= colors.CTHEME_1,
                width= self.taskcreator.height * 0.08,
                height= self.taskcreator.height * 0.08,
            ),
        )
        self.color_picker = ft.Container(
            border= ft.border.all(2, colors.WHITE_1),
            width= self.taskcreator.height * 0.13,
            height= self.taskcreator.height * 0.13,
            # border_radius= ft.border_radius.all(3),
            alignment= ft.alignment.center,
            bgcolor= None,
            on_click= self._color_picker_on_click
        )
        self.dropdown = ft.Dropdown(
            label= 'Priorities',
            border_width= 2,
            border_color= colors.WHITE_1,
            width= self.taskcreator.width * 0.40,
            menu_width= self.taskcreator.width * 0.40,
            menu_height= self.taskcreator._height * 0.60,
            text_size= fontsize.S2,
            enable_filter= True,
            editable= True,
            options= [],
            value= 'DEFAULT',
            on_change= self.update_priority,
        )
        self.annotation_input = ft.TextField(
            border= ft.InputBorder.UNDERLINE,
            border_color= colors.WHITE_1,
            text_size= fontsize.S2, 
            width= self.taskcreator.width * 0.80,
            # counter_text= '{value_length} / {max_length}',
            # max_length= 4096,
            on_change = self._annotation_on_change,
        )
        
        self.content = self._priority_build()

    def creat_priority(self, priority):
        self.taskcreator.controller.on_creat_priority(priority)
        pass

    def load_priorities(self):
        self.taskcreator.controller.on_load_priorities()
        pass

    def step_reset(self):
        icon = self.icon
        dropdown = self.dropdown
        picker = self.color_picker
        annotation = self.annotation_input

        dropdown.value = 'DEFAULT'
        icon.bgcolor = None
        icon.border = ft.border.all(2, colors.WHITE_1)
        icon.content.color = colors.CTHEME_1
        picker.bgcolor = None
        annotation.value = self.taskcreator.annotation
        self.load_priorities()
        pass

    def step_update(self):
        self.dropdown.options = self.options
        self.dropdown.update()
        
    def set_options(self, priorities):
        def icon(src, color):
            return ft.Image(
                src= src,
                fit= ft.ImageFit.CONTAIN,
                width= self.taskcreator.height * 0.05,
                height= self.taskcreator.height * 0.05,
                color= color,
            )
        def text(name, color):
            return ft.Text(
                name,
                color= color if color else colors.WHITE_2,
                size= fontsize.S3,
            )
        
        options = []
        all_priorities = {}
        for item in priorities:
            options.append(
                ft.DropdownOption(
                    key= item['name'],
                    leading_icon= icon(item['src'], item['color']),
                    content= text(item['name'], item['color']),
                    text= item['name'],
                )
            )
            all_priorities[item['name']] = item

        self.priorities = all_priorities
        self.options = options

    def update_options(self):
        dropdown = self.content.controls[0].controls[1].controls[1]
        options = self.get_options()

        dropdown.options = options
        dropdown.update()
        pass

    def next_btn_update(self):
        if self.taskcreator.priority is None:
            priority = self.priorities['DEFAULT']
            self.taskcreator.priority = priority

        if self.taskcreator.icon:
            src = self.taskcreator.icon.content.src

            self.priority_icon.content.src = src
            self.priority_icon.update()

        self.taskcreator.next.disabled = False
        self.taskcreator.next.update()

    def update_priority(self, e):
            priority = self.priorities[e.data]
            color = priority['color']

            if color:
                self.priority_icon.content.color = colors.WHITE_1
                self.priority_icon.bgcolor = color
                self.priority_icon.border = ft.border.all(2, colors.CDEFAULT)
            else:
                self.priority_icon.content.color = colors.CTHEME_1
                self.priority_icon.border = ft.border.all(2, colors.WHITE_1)
                self.priority_icon.bgcolor = color

            self.priority_picker.bgcolor = color
            self.priority_icon.update()
            self.priority_picker.update()
            self.taskcreator.priority = priority
    
    def _color_picker_on_click(self, e):
        print('color_picker_on_click:')

        priority = {
            'name': 'NOVAA',
            'color': '#036ad8'
        }
        self.creat_priority(priority)

    def _annotation_on_change(self, e):
        self.taskcreator.annotation = e.data
        pass

    def _priority_build(self):
        group1 = self.taskcreator._group()
        group2 = self.taskcreator._group()

        options = []

        icon = self.icon
        picker = self.color_picker
        dropdown = self.dropdown 
        text_input = self.annotation_input

        self.priority_icon = icon
        self.priority_picker = picker

        group1.controls[0].content.value = 'Select the priority: '
        group1.controls[1].controls = [
            icon,
            dropdown,
            picker,
        ]

        group2.controls[0].content.value = 'Annotation:'
        group2.controls[1].controls = [text_input]

        return ft.Column(
            spacing=0,
            controls=[
                group1,
                group2
            ]
        )