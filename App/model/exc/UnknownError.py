class UnknownError(Exception):
    def __init__(self, msg):
        super().__init__(f'*** Unknown error at the: {msg} ***')