class SchedDTO:
    def __init__(self, icon= None, name= None, date= None, duration= None, time= None, priority= None, annotation= None, sched_id=None):
        self.icon = icon
        self.name = name
        self.date = date
        self.duration = duration
        self.time = time
        self.priority = priority
        self.annotation = annotation
        self.sched_id = sched_id
        pass