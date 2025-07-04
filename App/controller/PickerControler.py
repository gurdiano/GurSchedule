from  App.view.components.DatePicker import DatePicker

class PickerController():
    def __init__(self, page):
        self.page = page
        self.view = DatePicker(self, page)
        self.page.pubsub.subscribe_topic('picker', self.hover_handler)

    def hover_handler(self, topic, message):
        self.view.display_date(message)
        pass
    
    def date_update(self, date):
        self.page.pubsub.send_all_on_topic('date-update', date)
        pass

    def picker_value_handler(self, topic, message):
        self.view.update_display(date= message)
        self.page.pubsub.send_all_on_topic('date-update', message)
        pass