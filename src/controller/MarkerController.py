import flet as ft
from  view.components.Marker import Marker

class MarkerController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.controls = [*[Marker(self, page, n) for n in range(24)]]
        self.add_sub()

    def add_sub(self):
        for marker in self.controls:
            self.page.pubsub.subscribe_topic(f'markers/{marker.data}', marker.highlight_marker)
        
