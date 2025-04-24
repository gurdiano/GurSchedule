class IntegrityError(Exception):
    def __init__(self, id, msg):
        super().__init__(msg)
        self.id = id