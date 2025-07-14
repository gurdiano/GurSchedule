class TaskConflicted(Exception):
    def __init__(self, scheds, msg):
        self.scheds = scheds
        
        super().__init__(msg)