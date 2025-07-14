import flet as ft

from view.resources.utility import colors, srcs, fontsize
from flet_contrib.color_picker import ColorPicker


class PriorityStep(ft.Container):
    def __init__(self, taskcreator, page):
        super().__init__()
        self.taskcreator = taskcreator
        self.page = page
        self.visible = False

        self.priorities = None
        self.options = None
        self.priority_icon = None

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
        self.color_picker_icon = ft.Container(
            border= ft.border.all(2, colors.WHITE_1),
            width= self.taskcreator.height * 0.13,
            height= self.taskcreator.height * 0.13,
            # border_radius= ft.border_radius.all(3),
            alignment= ft.alignment.center,
            bgcolor= None,
            on_click= self.open_color_picker
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
        
        self.color_picker = self._color_picker_build()
        self.content = self._priority_build()

    
    def creat_priority(self, e):
        text_input = ft.TextField(
            label= 'Name',
            hint_text= 'Default',
            border= colors.WHITE_1,
            width= self.taskcreator._width * 0.40,
            capitalization= ft.TextCapitalization.CHARACTERS,
        )

        def on_dismiss(e):
            last_priority_key = self.taskcreator.priority['name']
            last_priority = self.priorities[last_priority_key]
            text = text_input.value.strip()
            new_priority = None

            if text:
                new_priority = {
                    'name': text,
                    'src': srcs.USER,
                    'color': last_priority['color']
                }

            if new_priority:
                name = new_priority['name']
                icon_src = new_priority['src']

                if name in self.priorities:
                    self.dropdown.value = name
                    self.dropdown.data = name
                    self.taskcreator.priority = new_priority
                    self.update_priority(self.dropdown)
                    self.dropdown.update()
                    return
                
                new_option = ft.DropdownOption(
                    key= name,
                    text= name,
                    leading_icon= ft.Image(
                        src= icon_src,
                        fit= ft.ImageFit.CONTAIN,
                        width= self.taskcreator._height * 0.05,
                        height= self.taskcreator._height * 0.05,
                        color= colors.WHITE_2,
                    ),
                    content= ft.Text(
                        name,
                        color= colors.WHITE_2,
                        size= fontsize.S3,
                    ),
                )

                if name not in self.priorities:
                    self.options.insert(1, new_option)
                    self.taskcreator.priority = new_priority
                    self.priorities[name] = new_priority
                    self.dropdown.value = name
                    self.dropdown.update()
            else:
                self.dropdown.value = last_priority_key
                self.dropdown.update()

        def close_dialog(e):
            self.page.close(dialog)
            on_dismiss(e)

        dialog = ft.AlertDialog(
            bgcolor= '#00000000',
            content= ft.Container(
                bgcolor= colors.FLET_DEFAULT,
                width= self.taskcreator._width * 0.45,
                height= self.taskcreator._height * 0.40,
                alignment= ft.alignment.center,
                border_radius= ft.border_radius.all(5),

                content= ft.Column(
                    width= self.taskcreator._width * 0.40,
                    alignment= ft.MainAxisAlignment.CENTER,

                    controls = [
                        ft.Row(
                            alignment= ft.MainAxisAlignment.END,
                            height= self.taskcreator._height * 0.05,

                            controls=[
                                ft.Container(
                                    content= ft.Image(
                                        src= srcs.X_MARK,
                                        color= 'red',
                                        fit= ft.ImageFit.CONTAIN,
                                        width= self.taskcreator._height * 0.05,
                                        height= self.taskcreator._height * 0.05,
                                    ),
                                    alignment= ft.alignment.center_right,
                                    on_click= close_dialog,
                                ),
                            ],
                        ),
                        ft.Text(
                            value= 'Define a name for Priority: ',
                            color= colors.WHITE_1,
                            size= fontsize.S2_02,
                        ),
                        text_input,
                    ],
                ),
            ),
            on_dismiss= on_dismiss,
        )

        self.page.open(dialog)
        pass

    def load_priorities(self):
        self.taskcreator.controller.on_load_priorities()
        pass

    def step_reset(self):
        icon = self.icon
        dropdown = self.dropdown
        picker = self.color_picker_icon
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

        add_option = ft.DropdownOption(
            key= 'ADD PRIORITY',
            leading_icon= icon(srcs.PLUS, colors.WHITE_1),
            content= text('ADD PRIORITY', colors.WHITE_2),
            text= 'ADD PRIORITY',
        )
        options.insert(0, add_option)
        self.options = options
        pass

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
            if e.data == 'ADD PRIORITY':
                self.creat_priority(e)
                return
            
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

            self.color_picker_icon.bgcolor = color
            self.priority_icon.update()
            self.color_picker_icon.update()
            self.taskcreator.priority = priority
    
    def open_color_picker(self, e):
        color_picker_control = self.color_picker.data
        color = color_picker_control.color 
        
        priority = self.taskcreator.priority

        if priority['color'] != None:
            color_picker_control.color = priority['color']
  
        def update_priority_color(e):
            new_color = color_picker_control.color
            if priority['name'] == 'DEFAULT':
                _priority = self.priorities['PERSONAL']
                self.dropdown.value = 'PERSONAL'
                self.dropdown.update()
                self.taskcreator.priority = _priority

            if  new_color != color:
                self.color_picker_icon.bgcolor = new_color
                self.icon.bgcolor = new_color
                self.icon.content.color = colors.WHITE_1
                self.color_picker_icon.update()
                self.icon.update()
                self.taskcreator.priority['color'] = new_color

        self._update_recent_colors_pick()

        self.page.open(
            ft.AlertDialog(
                bgcolor= '#00000000',
                content= self.color_picker,
                on_dismiss= update_priority_color,
            )
        )

    def _annotation_on_change(self, e):
        self.taskcreator.annotation = e.data
        pass
    
    def _update_recent_colors_pick(self):
        recent_colors_control = self.color_picker.content.controls[1].controls
        options = self.options
        priorities = self.priorities

        last_colors = []
        op_len = len(options)
        control_len = len(recent_colors_control)
        for n in range(op_len, op_len if op_len > control_len else 0, -1):
            if n != 1: #'ADD PRIORITY'
                name = options[n-1].key
                color = priorities[name]['color']
                last_colors.append(color)

        for i in range(len(last_colors)):
            if last_colors[i]: recent_colors_control[i].bgcolor = last_colors[i]

    def _color_picker_build(self):
        color_picker = ColorPicker(color= "#c8df6f")

        # slot
        _colors = [
            '#272a2f',
            '#272a2f',
            '#272a2f',
            '#272a2f',
            '#272a2f',
            '#272a2f',
            '#272a2f',
            '#272a2f',
        ]

        def on_click(e):
            color_picker.color = e.control.bgcolor
            color_picker.update()

        recent_colors = []
        space = 5
        size = (color_picker.width / len(_colors)) - (space * 2)
        for color in _colors:
            recent_colors.append(
                ft.Container(
                    border= ft.border.all(1, 'black'),
                    border_radius= ft.border_radius.all(2),
                    width= size,
                    height= size,
                    bgcolor= color,
                    margin= space,
                    on_click= on_click,
                )
            )
        
        return ft.Container(
            bgcolor= colors.FLET_DEFAULT,
            content= ft.Column(
                controls=[
                    color_picker,

                    ft.Row(
                        spacing= 0,
                        width= color_picker.width,
                        alignment= ft.MainAxisAlignment.CENTER,
                        vertical_alignment= ft.CrossAxisAlignment.CENTER,
                        controls=recent_colors,
                    ),
                ],
            ),

            height= self.taskcreator._height * 1.05,
            data = color_picker,
        )
    
    def _priority_build(self):
        group1 = self.taskcreator._group()
        group2 = self.taskcreator._group()

        options = []

        icon = self.icon
        picker = self.color_picker_icon
        dropdown = self.dropdown 
        text_input = self.annotation_input

        self.priority_icon = icon

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