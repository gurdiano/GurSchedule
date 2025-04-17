class ResourceNotFound(Exception):
    def __init__(self, id, msg="{} was not found!"):
        super().__init__(msg.format(id)) 

class CreateException(Exception):
    def __init__(self, id, msg="{} is an invalid input or already exists!"):
        super().__init__(msg.format(id))

class ExceedsOneDay(Exception):
    def __init__(self, id, msg="{}h error - The task cannot be extended to another day"):
        super().__init__(msg.format(id))

class ConflictingTasks(Exception):
    def __init__(self, id, msg="These tasks are conflicting! {}"):
        super().__init__(msg.format(id))
