class CreateBaseException(Exception):
    def __init__(self, msg='Error in create base.'):
        super().__init__(msg)