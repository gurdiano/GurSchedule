import flet as ft
import threading
import pystray as st
from PIL import Image

from App.controller.LayoutController import LayoutController
from App.model.init_db import initialize_database

def system_stray_icon(page):
    def on_show():
        page.window.visible = True
        page.window.to_front = True
        page.update()

    def on_exit():
        page.window.destroy()

    icon_img = Image.open(r'App\view\resources\img\pen-svgrepo.png')
    menu = st.Menu(
        st.MenuItem('Show', lambda icon, item: on_show()),
        st.MenuItem('Exit', lambda icon, item: on_exit()),
    )
    return st.Icon(name='GurSchedule', icon=icon_img, menu=menu)

def main(page: ft.Page):
    page.title = "GurSchedule"
    page.padding = 0
    page.window.frameless = True
    page.window.width = 1356
    page.window.height = 678

    page.window.bgcolor = ft.Colors.TRANSPARENT
    page.bgcolor = ft.Colors.TRANSPARENT
    page.window.maximizable = False
    page.window.skip_task_bar = True
    
    controller = LayoutController(page)

    page.add(
        controller.view.build()
    )

    def start_tray():
        system_stray_icon(page).run()

    threading.Thread(target=start_tray, daemon= True).start()

initialize_database()
ft.app(main)