import flet as ft

import App.FrontEnd.Components.Models.models as comp

from App.FrontEnd.Components.Wrapper.Day import Day
from App.FrontEnd.Components.Wrapper.Hour import Hour

from App.FrontEnd.Components.Sidebar.Sidebar import Sidebar    
from App.FrontEnd.Components.Sidebar.Datepicker import Datepicker    
from App.FrontEnd.Components.Sidebar.Wrapper import Wrapper    
from App.FrontEnd.Components.Sidebar.Hour import Hour as Hourmarker   

# from App.FrontEnd.Components.Taskcreator.Task import Task
from App.FrontEnd.Components.Taskcreator.Beginning import Beginning
from App.FrontEnd.Components.Taskcreator.Duration import Duration

from App.FrontEnd.Services.Communication import comm

preto_menos_preto = '#020202'
preto_com_brancodes = '#0a0a0a' 
gelo = '#e0e0e0'
tipo_vinho = '#3c3537'
pink = '#e91e63'
branco = 'white'
verde = '#4caf50'
preto = 'black'

#PICKER
COR_DO_CARD = preto_com_brancodes
COR_DOS_NUM = gelo
COR_TITULO = pink
COR_DA_LINHA = COR_TITULO
COR_SELEÇÃO =  COR_TITULO
SELC_DESTAQUE = branco

#OUTROS
COR_DE_FUNDO = preto
COR_TASK_CON =  preto_menos_preto
HOVER_TASK_CON = preto_com_brancodes

def main(page: ft.Page):
    page.title = "GurSchedule"
    page.window.width = 1250            
    page.window.height = 712 

    # page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.padding = 0
    page.spacing = 0

    page.window.resizable = True
    page.window.frameless = True

    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(

            ###Usando
            primary=COR_SELEÇÃO,
            on_primary=SELC_DESTAQUE,
            on_surface=COR_DOS_NUM,
            on_surface_variant=COR_TITULO,
            outline_variant=COR_DA_LINHA,

            # background='pink',
            # secondary='pink',
            # tertiary='pink',

            # primary_container='pink',
            # inverse_primary='pink',
            # inverse_surface='pink',
            
            # error='pink',
            # error_container='pink',

            # on_background='pink',
            # on_error='pink',
            # on_error_container='pink',
            # on_inverse_surface='pink',
            
            # on_primary_container='pink',
            # on_secondary='pink',
            # on_secondary_container='pink',
            

            # on_tertiary='pink',
            # on_tertiary_container='pink',
            # outline='pink',
            # scrim='pink',
            # secondary_container='pink',
            # shadow='pink',
            # surface='pink',
            # surface_tint='pink',
            # surface_variant='pink',
            # tertiary_container='pink',
        ),

        card_theme=ft.CardTheme(
            color=COR_DO_CARD,
        ),

        banner_theme=ft.BannerTheme(
            bgcolor='#0a0a0a'
        ),

        date_picker_theme=ft.DatePickerTheme(
            bgcolor='green',
            day_bgcolor='green',
            year_bgcolor='green',
            today_bgcolor='green',
            header_bgcolor='green',
            range_picker_bgcolor='green',
            range_selection_bgcolor='green',
            range_picker_header_bgcolor='green'
        )
    )
    
    def main_frame(width, height):
        window = ft.Container(
            width=width,
            height=height,
            bgcolor="pink",
            alignment=ft.alignment.center_left,
        )
        
        #Left content -> begin
        sidebar = Sidebar(
            father=window
        )

        sidewrapper = Wrapper(
            father=sidebar
        )

        datepicker = Datepicker(
            father=sidebar.header,
            page=page
        )

        marker_content = []
        for hh in range(24):
            marker = Hourmarker(
                father=sidewrapper.hours_container,
                value=hh
            )
            marker_content.append(marker)
 
        sidewrapper.hours = marker_content
        sidebar.header = datepicker
        sidebar.wrapper = sidewrapper
        #Left content -> end

        #Right content -> begin
        wrapper = comp.wrapper(window)
        wrapper_content = comp.main_content(wrapper)
        wrapper_footer = comp.wrapper_footer(wrapper)

        wrapper.content = ft.Column(
            spacing=0,

            controls= [
                wrapper_content,
                wrapper_footer,
            ]
        )

        #Full week "7 days" -> begin 
        days = []
        for dd in range(7):
            day = Day(
                father=wrapper_content,
                value=(dd + 1)
            )
            _title = comp.header(
                father=day.view,
                num=(dd + 1)
            )

            hours = [_title]
            for hh in range(24):
                hour = Hour(
                    father=day,
                    value=hh
                )
                hours.append(hour.view)

            day.view.content = ft.Column(
                spacing=0,
                controls=hours
            )
            days.append(day.view)
        #Full week "7 days" -> end 
        
        #Right content -> end 

        #Communication -> begin
        comm.hours = marker_content
        comm.datepicker = datepicker
        comm.window = window
        comm.page = page
        #Communication -> end 
        
        wrapper_content.content = ft.Row(
            spacing=0,
            controls=days
        )

        window.content = ft.Row(
            spacing=0,

            controls= [
                sidebar.view,
                wrapper
            ]
        )

        return window

    # FRAME PRINCIPAL CASO QUEIRA MUDAR...
    frame = ft.Container(
        content=main_frame(page.window.width, page.window.height)
    )

    # EVENTO PARA ARRASTAR
    def on_resize(e):
        frame.content = main_frame(page.window.width, page.window.height)
        page.update()

    page.on_resized = on_resize

    # ADD FRAM NA PAGE
    page.add(
        ft.WindowDragArea(
            frame
        )
    )

    
ft.app(target=main)