import flet as ft

def row1(father: ft.Container):
    return ft.Container(
        # border=ft.border.all(1, 'white'),

        width = father.width,
        height = father.height * 0.05,
        alignment= ft.alignment.center_left

    )

def row2(father: ft.Container):
    return ft.Container(
        # border=ft.border.all(1, 'blue'),

        width = father.width,
        height = father.height * 0.87,
        alignment= ft.alignment.top_left
    )

def row3(father: ft.Container):
    return ft.Container(
        # border=ft.border.all(1, 'white'),

        width = father.width,
        height = father.height * 0.08,
        alignment=ft.alignment.top_center,
    )

def row4(father: ft.Container):
    return ft.Container(
        # border=ft.border.all(0.5, 'black'),

        width = father.width,
        height = father.height * 0.50,
    )

def row5(father: ft.Container):
    return ft.Container(
        # border=ft.border.all(1, 'white'),

        width = father.width,
        height = father.height * 0.04166,
    )

def col1(father: ft.Container):
    return ft.Container(
        # border=ft.border.all(1, 'white'),

        width = father.width * 0.08,
        height = father.height,
    )

def col2(father: ft.Container):
    return ft.Container(
        # border=ft.border.all(1, 'white'),

        width = father.width * 0.13142,
        height = father.height,
    )
    
def col3(father: ft.Container):
    return ft.Container(
        # border=ft.border.all(1, 'white'),

        width = father.width * 0.50,
        height = father.height,
    )

def col4(father: ft.Container):
    return ft.Container(
        # border=ft.border.all(1, 'white'),
        
        width = father.width * 0.92,
        height = father.height,
    )

