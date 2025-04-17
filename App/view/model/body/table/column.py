import flet as ft 
from App.view.model.dividers import col2
from App.view.utility.colors import *

def column(father: ft.Column):
    container = col2(father)
    container.bgcolor = black_0

    return container