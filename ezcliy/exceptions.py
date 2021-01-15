class MessageableException(Exception):
    message: str


class MissingPositional(MessageableException):
    def __init__(self, positional, position):
        self.positional = positional
        self.position: int = position
        self.message = f'Missing {position+1}. argument!'

