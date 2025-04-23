from  App.view.components.DatePicker import DatePicker

class PickerController():
    def __init__(self, page):
        self.page = page
        self.view = DatePicker(self, page)
        self.page.pubsub.subscribe_topic('picker', self.hover_handler)

    def hover_handler(self, topic, message):
        self.view.display_date(message)