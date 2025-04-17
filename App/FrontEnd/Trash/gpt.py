import flet as ft

def main(page: ft.Page):

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def on_hooover(e):
        if e.data == "true":
            e.control.bgcolor = "pink"
        else:
            e.control.bgcolor = "green"
        
        page.update()


    cont = ft.Container(
        width=300,
        height=100,
        bgcolor="blue",
        on_hover=on_hooover
    )

    

    

    page.add(
        cont
    )

ft.app(main)

def gpt_validadas():

    rotate=ft.transform.Rotate(-1.5708) ##roda 90graus
    alignment=ft.alignment.center ##"alinha no centro"

    ##texto
    text = ft.Text(
        "Texto em 90 graus",
        color=ft.colors.WHITE,
        size=56,
    )

    ##imagem
    svg_image = ft.Image(
        src=r"App\Sources\Resources\dawn.svg",
        width=225,
        height=795
    )

    ##borda
    border=ft.border(
            top=ft.border.BorderSide(1, ft.colors.BLACK), 
            bottom=ft.border.BorderSide(1, ft.colors.BLACK)
        ),
    
    border=ft.border.all(1, ft.colors.BLACK)

    ##p/ borda redonda
    border_radius=ft.border_radius.all(3)
    
    ## Janela sem borda
    # page.window.frameless = True

    ## redemenciona
    # def on_resize(e):
    #     window.width = page.window.width
    #     window.height = page.window.height
    #     page.update()

    # page.on_resize = on_resize

    # page.add(
    #     ft.WindowDragArea(
    #         window
    #     )
    # )

    pass
