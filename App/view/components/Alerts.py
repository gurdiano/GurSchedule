import flet as ft
import datetime
import time

from App.view.resources.utility import colors, fontsize, srcs, dividers
from App.view.resources.utility.dicts import month_english

class Alerts:
    def __init__(self, page):
        self.page = page
        #TaskDetails sizes:
        self.width = dividers.APP_LAYOUT_WIDTH * 0.50 
        self.height = dividers.APP_LAYOUT_HEIGHT * 0.90
        #standard sizes:
        self.dialog_width = self.width * 0.90
        self.dialog_height = self.height * 0.40

        self.content = ft.Container(
            expand= True,
        )
        self.header = ft.Row(
            width= self.dialog_width * 0.95,
            height= self.dialog_height * 0.15,
            alignment= ft.MainAxisAlignment.CENTER,
            vertical_alignment= ft.CrossAxisAlignment.CENTER,

            controls= [
                ft.Container(
                    width= self.dialog_width * 0.85,
                    height= self.dialog_height * 0.15,
                    alignment= ft.alignment.bottom_center,
                    content= ft.Text(
                        value = 'Confirm Schedule.',
                        color= colors.WHITE_2,
                        size= fontsize.S2_02,
                    ),
                ),
                ft.Container(
                    content= ft.Image(
                        src= srcs.X_MARK,
                        color= 'red',
                        fit= ft.ImageFit.CONTAIN,
                        width= self.dialog_height * 0.05,
                        height= self.dialog_height * 0.05,
                    ),
                    on_click= self.close_dialog,
                ),
            ],
        )
        self.cancel_btn = ft.CupertinoButton(
            width= self.dialog_width * 0.20,
            height= self.dialog_height * 0.20,
            bgcolor= colors.CDEFAULT,
            content= ft.Text(
                value= 'Cancel',
                color= colors.WHITE_2,
                size= fontsize.S2_02,
            ),
            on_click= self.close_dialog,
        )
        self.ok_btn = ft.CupertinoButton(
            width= self.dialog_width * 0.20,
            height= self.dialog_height * 0.20,
            bgcolor= colors.CTHEME_1,
            content= ft.Text(
                value= 'Ok',
                color= colors.WHITE_2,
                size= fontsize.S2_02,
            ),
        )
        self.btns = ft.Row(
            width= self.dialog_width * 0.90,
            height= self.dialog_height * 0.30,
            controls= [self.cancel_btn, self.ok_btn],
            alignment= ft.MainAxisAlignment.END,
            vertical_alignment= ft.CrossAxisAlignment.START,
        )
        self.body = ft.Container(
            width= self.dialog_width,
            height= self.dialog_height,
            bgcolor= colors.BLACK_1,
            border= ft.border.all(1, colors.BLACK_3),
            content = ft.Column(
                horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                alignment= ft.MainAxisAlignment.END,
                controls= [
                    self.header,
                    self.content,
                    self.btns,
                ],
            ),
        )
        self.dialog = ft.AlertDialog(
            bgcolor= '#00000000',
            on_dismiss= self.close_dialog,
            content= self.body,
        )
    
    def reset(self):
        self.body.width = self.dialog_width
        self.body.height = self.dialog_height
        self.btns.controls = [self.cancel_btn, self.ok_btn,]
        self.ok_btn.on_click = None
        pass

    def close_dialog(self, e):
        self.page.close(self.dialog)
        pass

    def open_confirm(self, time, name, event):
        self.reset()
        dialog_width = self.width * 0.90
        dialog_height = self.height * 0.40

        hour_str = time.hour if  time.hour > 9 else f'0{time.hour}'
        min_str = time.minute if time.minute > 9 else f'0{time.minute}'

        def confirm_dialog(e):
            self.page.close(self.dialog)
            event()
        self.ok_btn.on_click = confirm_dialog

        msg = ft.Row(
            controls= [
                ft.Text(
                    value= f"Are you sure you want set ",
                    color= colors.WHITE_2,
                    size= fontsize.S2_02,
                ),
                ft.Text(
                    value= f"'{name}'",
                    color= colors.CTHEME_1,
                    size= fontsize.S2_02,
                ),
                ft.Text(
                    value= f" for ",
                    color= colors.WHITE_2,
                    size= fontsize.S2_02,
                ),
                ft.Text(
                    value= f"'{hour_str}: {min_str}'",
                    color= colors.CTHEME_1,
                    size= fontsize.S2_02,
                ),
                ft.Text(
                    value= f" h?",
                    color= colors.WHITE_2,
                    size= fontsize.S2_02,
                ),
            ],

            width= dialog_width * 0.95,
            alignment= ft.MainAxisAlignment.CENTER,
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
            expand= True,
            spacing= 0,
        )
        self.content.content = msg
        self.page.open(self.dialog)
        pass

    def open_confirm_bulk(self, text, event):
        self.reset()
        dialog_width = self.width * 0.90
        dialog_height = self.height * 0.40

        def confirm_dialog(e):
            self.page.close(self.dialog)
            event()
        self.ok_btn.on_click = confirm_dialog

        msg = ft.Row(
            controls= [
                ft.Text(
                    value= f"Are you sure you want to",
                    color= colors.WHITE_2,
                    size= fontsize.S2_02,
                    no_wrap= False,
                ),
                ft.Text(
                    value= f" {text} ",
                    color= colors.CTHEME_1,
                    size= fontsize.S2_02,
                    no_wrap= False,
                ),
                ft.Text(
                    value= f"the selected schedule?",
                    color= colors.WHITE_2,
                    size= fontsize.S2_02,
                    no_wrap= False,
                ),
            ],
            width= dialog_width * 0.95,
            alignment= ft.MainAxisAlignment.CENTER,
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
            expand= True,
            spacing= 0,
        )

        self.content.content = msg
        self.page.open(self.dialog)
        pass

    def open_creation_success(self, name):
        self.reset()
        dialog_width = self.width * 0.90
        dialog_height = self.height * 0.40
        
        def confirm_dialog(e):
            self.page.close(self.dialog)

        self.ok_btn.on_click = confirm_dialog

        msg = ft.Row(
            controls= [
                ft.Text(
                    value= f"The schedule ",
                    color= colors.WHITE_2,
                    size= fontsize.S2_02,
                ),
                ft.Text(
                    value= f"'{name}'",
                    color= colors.CTHEME_1,
                    size= fontsize.S2_02,
                ),
                ft.Text(
                    value= f" was created successfully!",
                    color= colors.WHITE_2,
                    size= fontsize.S2_02,
                ),
            ],

            width= dialog_width * 0.95,
            alignment= ft.MainAxisAlignment.CENTER,
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
            expand= True,
            spacing= 0,
        )

        self.btns.controls.pop(0)
        self.content.content = msg
        self.page.open(self.dialog)
        pass

    def open_creation_fail(self, name):
        self.reset()
        dialog_width = self.width * 0.90
        dialog_height = self.height * 0.40

        msg = ft.Row(
            controls= [
                ft.Text(
                    value= f"Failed to create schedule ",
                    color= colors.WHITE_2,
                    size= fontsize.S2_02,
                ),
                ft.Text(
                    value= f"'{name}'",
                    color= colors.CTHEME_1,
                    size= fontsize.S2_02,
                ),
                ft.Text(
                    value= f".",
                    color= colors.WHITE_2,
                    size= fontsize.S2_02,
                ),
            ],
            width= dialog_width * 0.95,
            alignment= ft.MainAxisAlignment.CENTER,
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
            expand= True,
            spacing= 0,
        )
        self.btns.controls.pop(0)
        self.content.content = msg
        self.page.open(self.dialog)
        pass

    def open_edit_confirm(self, time, date, old_name, event):
        self.reset()
        dialog_width = self.width * 0.90
        dialog_height = self.height * 0.40

        def confirm_dialog(e):
            self.page.close(self.dialog)
            event()

        self.ok_btn.on_click = confirm_dialog

        old_hour_str = time.hour if time.hour > 9 else f'0{time.hour}'
        old_min_str = time.minute if time.minute > 9 else f'0{time.minute}'
        old_date = f'{month_english[date.month]} {date.day}'

        msg = ft.Row(
            controls= [
                ft.Text(
                    value= f"Are you sure you want to edit ",
                    color= colors.WHITE_2,
                    size= fontsize.S2_02,
                ),
                ft.Text(
                    value= f"'{old_name}' - {old_date} at {old_hour_str}: {old_min_str}h ",
                    color= colors.CTHEME_1,
                    size= fontsize.S2_02,
                ),
                ft.Text(
                    value= f"? ",
                    color= colors.WHITE_2,
                    size= fontsize.S2_02,
                ),
            ],
            width= dialog_width * 0.95,
            alignment= ft.MainAxisAlignment.CENTER,
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
            expand= True,
            spacing= 0,
        )

        self.content.content = msg
        self.page.open(self.dialog)
        pass

    def open_remove_confirm(self, name, event):
        self.reset()
        dialog_width = self.width * 0.90
        dialog_height = self.height * 0.40

        def confirm_dialog(e):
            self.page.close(self.dialog)
            time.sleep(0.1)
            self.page.overlay.clear()
            self.page.update()
            event()

        self.ok_btn.on_click = confirm_dialog

        msg = ft.Row(
            controls= [
                ft.Text(
                    value= f"Are you sure you want remove schedule ",
                    color= colors.WHITE_2,
                    size= fontsize.S2_02,
                ),
                ft.Text(
                    value= f"'{name}'",
                    color= 'red',
                    size= fontsize.S2_02,
                ),
                ft.Text(
                    value= f"?",
                    color= colors.WHITE_2,
                    size= fontsize.S2_02,
                ),
            ],

            width= dialog_width * 0.95,
            alignment= ft.MainAxisAlignment.CENTER,
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
            expand= True,
            spacing= 0,
        )

        self.content.content = msg
        self.page.open(self.dialog)
        pass
    
    def open_overwrite_confirm(self, name, event, scheds=None):
        self.reset()
        dialog_width = self.width * 0.90
        dialog_height = self.height * 0.40
        
        conflicts_column = ft.Column()
        for _sched in scheds:
            pre = datetime.datetime.combine(datetime.date.today(), _sched.time)
            pos = pre + datetime.timedelta(minutes= _sched.duration)
            date = f'{month_english[_sched.date.month]} {_sched.date.day}' 

            pre_hour = pre.hour if pre.hour > 9 else f'0{pre.hour}'
            pre_minute = pre.minute if pre.minute > 9 else f'0{pre.minute}'
            pos_hour = pos.hour if pos.hour > 9 else f'0{pos.hour}'
            pos_minute = pos.minute if pos.minute > 9 else f'0{pos.minute}'

            conflicts_column.controls.append(
                ft.Text(
                    value= f" '{_sched.name}' - {date} from {pre_hour}: {pre_minute}h to {pos_hour}: {pos_minute}h",
                    color= 'red',
                    size= fontsize.S2_02,
                )
            )
        conflicts_column.width = dialog_width * 0.80
        conflicts_column.height = dialog_height * 0.30
        conflicts_column.scroll = ft.ScrollMode.ALWAYS
        conflicts_column.horizontal_alignment = ft.CrossAxisAlignment.START
        conflicts_column.spacing = dialog_height * 0.01

        def confirm_dialog(e):
            self.page.close(self.dialog)
            event()
        self.ok_btn.on_click = confirm_dialog

        msg = ft.Row(
            controls= [
                ft.Text(
                    value= f"'{name if len(name) <=8 else f'{name[:8]}...'}' ",
                    color= colors.CTHEME_1,
                    size= fontsize.S2_02,
                ),
                ft.Text(
                    value= f"conflicts with the following scheduled activities. Do you want to overwrite them?",
                    color= colors.WHITE_2,
                    size= fontsize.S2_02,
                ),
            ],
            width= dialog_width * 0.95,
            alignment= ft.MainAxisAlignment.CENTER,
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
            expand= True,
            spacing= 0,
        )
        self.content.content = ft.Column(
            controls= [
                msg,
                conflicts_column,
            ],

            spacing= 0,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        )

        self.page.open(self.dialog)
        pass