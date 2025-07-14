import flet as ft
import os
import shutil

from view.resources.utility import colors, srcs, fontsize

class MoreIcons(ft.Container):
    def __init__(self, parent, page, row, all_icons):
        super().__init__()
        self.parent = parent
        self.page = page
        self.row = row
        self.all_icons = all_icons
        self.is_open = False

        self.file_picker = ft.FilePicker(on_result= self.on_file_picked)

        self.upload_icon =  ft.Container(
            height= self.parent.taskcreator._height * 0.15,
            width= self.parent.taskcreator._height * 0.60,
            bgcolor= colors.CDEFAULT,
            border= ft.border.all(1, colors.BLACK_0),
            border_radius= ft.border_radius.all(5),
            alignment= ft.alignment.center,

            content= ft.Row(
                alignment= ft.MainAxisAlignment.CENTER,
                vertical_alignment= ft.CrossAxisAlignment.CENTER,

                controls= [
                    ft.Image(
                        src= srcs.UPLOAD,
                        fit= ft.ImageFit.CONTAIN,
                        height= (self.parent.taskcreator._height * 0.15) * 0.40,
                        width= (self.parent.taskcreator._height * 0.15) * 0.40,
                        color= colors.WHITE_1,
                    ),
                    ft.Text(
                        value= 'Upload Icon.svg',
                        color= colors.WHITE_1,
                        size= fontsize.S2,
                    ),
                ],
            ),
        )
        self.x_mark_btn = ft.Container(
            width= self.parent.taskcreator.width * 0.05,
            alignment= ft.alignment.center,

            content= ft.Image(
                src= srcs.X_MARK,
                fit= ft.ImageFit.CONTAIN,
                color= colors.WHITE_1,
                height= self.parent.taskcreator.height * 0.03,
                width= self.parent.taskcreator.height * 0.03,
            ),
        )
        self.icons_control =  ft.Column(
            width= self.parent.taskcreator._width * 0.77,
            height= self.parent.taskcreator.height * 0.95,
            spacing= 0,
            scroll= ft.ScrollMode.ALWAYS,

            controls = self.all_icons,
        )

        self.content = ft.Container(
            bgcolor= colors.FLET_DEFAULT,
            width= self.page.window.width * 0.40,
            border_radius= ft.border_radius.all(10),
            alignment= ft.alignment.center,

            content= ft.Column(
                spacing= 0,
                controls= [
                    ft.Row(
                        width = self.parent.taskcreator._width * 0.77,
                        height= self.parent.taskcreator.height * 0.05,
                        alignment= ft.MainAxisAlignment.END,

                        controls= [self.x_mark_btn]
                    ),

                    self.icons_control,
                ],
            ),
        )

    def on_file_picked(self, e: ft.FilePickerResultEvent):
        folder = r'svg\person'
        if not os.path.exists(folder): os.makedirs(folder)

        if e.files:
            control = self.icons_control.controls
            upload_row = control.pop()

            for file in e.files:
                try:
                    save_path = os.path.join(folder, file.name)
                    new_icon = self.parent.taskcreator._icon2(src=save_path)
                    shutil.copyfile(file.path, save_path)

                    src = self.parent.creat_icon(save_path)

                    if src:
                        last_row = control[-1]
                        
                        if len(last_row.controls) < 8: 
                            last_row.controls.append(new_icon)
                        else:
                            row = ft.Row(
                                width=self.parent.taskcreator._width * 0.80,
                                spacing=self.parent.taskcreator._width * 0.02,
                            )
                            row.controls.append(new_icon)
                            control.append(row)
                except Exception:
                    None

            self.icons_control.controls.append(upload_row)
            self.icons_control.update()
        pass

    def close_dialog(self, e, dialog, ini_icon):
        if not self.is_open: return

        if self.parent.taskcreator.icon and self.parent.taskcreator.icon != ini_icon:
            self.row.controls.pop(6)
            _icon = self.parent.taskcreator._icon2(src= self.parent.taskcreator.icon.data)
            _icon.controls[0].bgcolor = colors.CTHEME_1
            self.parent.taskcreator.icon = _icon.controls[0]    

            self.row.controls.insert(0, _icon)
            self.row.update()
            self.is_open = False

        self.parent.page.close(dialog)
        pass

    def build(self):
        ini_icon = self.parent.taskcreator.icon

        _new_row = ft.Row(
            width=self.parent.taskcreator._width * 0.80,
            height=self.parent.taskcreator._height * 0.15,
            alignment= ft.MainAxisAlignment.CENTER,
            vertical_alignment= ft.CrossAxisAlignment.END,

            spacing=self.parent.taskcreator._width * 0.02,
            controls = [self.upload_icon],
        )
        self.icons_control.controls.append(_new_row)

        self.upload_icon.on_click= lambda e: self.file_picker.pick_files(
            allow_multiple= True,
            allowed_extensions= ['svg']
        )

        dialog = ft.AlertDialog(
            bgcolor= '#00000000',

            content= self.content,
        )

        self.x_mark_btn.on_click= lambda e: self.close_dialog(e, dialog, ini_icon)
        dialog.on_dismiss = lambda e: self.close_dialog(e, dialog, ini_icon)

        self.page.overlay.append(self.file_picker)
        self.page.open(dialog)
        self.is_open = True
        pass