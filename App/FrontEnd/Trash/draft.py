import flet as ft

def main(page: ft.Page):
    page.title = "Tabela Interativa"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    
    # Dados da tabela
    column_labels = ["mostrador", "A", "B", "D"]
    row_labels = ["mostrador", "1", "2", "3"]
    
    # Criar a tabela
    table = ft.Column(spacing=0)
    
    # Função para criar células com interação
    def create_cell(row, col, is_header=False):
        if row == 0 and col == 0:  # Canto superior esquerdo
            content = ft.Text(column_labels[0], weight="bold")
        elif row == 0:  # Cabeçalho de coluna
            content = ft.Text(column_labels[col], weight="bold")
        elif col == 0:  # Cabeçalho de linha
            content = ft.Text(row_labels[row], weight="bold")
        else:  # Célula normal
            content = ft.Text("")
        
        cell = ft.Container(
            content=content,
            width=100,
            height=50,
            alignment=ft.alignment.center,
            border=ft.border.all(1, ft.colors.BLACK),
            bgcolor=ft.colors.WHITE if not is_header else ft.colors.GREY_300,
            on_hover=lambda e, r=row, c=col: highlight_cells(e, r, c),
            data={"row": row, "col": col}
        )
        return cell
    
    # Função para destacar células
    def highlight_cells(e, row, col):
        # Resetar todas as células
        for table_row in table.controls:
            for cell in table_row.controls:
                cell.bgcolor = (
                    ft.colors.GREY_300 
                    if cell.data["row"] == 0 or cell.data["col"] == 0 
                    else ft.colors.WHITE
                )
                cell.content.color = ft.colors.BLACK
                cell.update()
        
        # Se não for cabeçalho, destacar apenas os marcadores e célula atual
        if row > 0 and col > 0:
            # Atualizar o mostrador
            mostrador = f"{column_labels[col]}{row_labels[row]}"
            table.controls[0].controls[0].content.value = mostrador
            table.controls[0].controls[0].update()
            
            # Destacar apenas os marcadores correspondentes
            table.controls[0].controls[col].bgcolor = ft.colors.AMBER_300  # Cabeçalho coluna
            table.controls[row].controls[0].bgcolor = ft.colors.AMBER_300  # Cabeçalho linha
            
            # Destacar a célula atual
            table.controls[row].controls[col].bgcolor = ft.colors.AMBER_200
            
            # Atualizar apenas as células modificadas
            table.controls[0].controls[col].update()
            table.controls[row].controls[0].update()
            table.controls[row].controls[col].update()
    
    # Construir a tabela
    for row in range(4):
        table_row = ft.Row(spacing=0)
        for col in range(4):
            is_header = row == 0 or col == 0
            table_row.controls.append(create_cell(row, col, is_header))
        table.controls.append(table_row)
    
    page.add(
        ft.Text("Passe o mouse sobre as células para ver a interação", size=16),
        ft.Divider(height=20, color=ft.colors.TRANSPARENT),
        table
    )

ft.app(target=main)