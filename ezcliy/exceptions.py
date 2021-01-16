class MessageableException(Exception):
    """
    Base class for user related errors.
    """
    message: str


class MissingPositional(MessageableException):
    """
    Raised when user forgets to pass positional.
    """
    def __init__(self, positional, position):
        """

        :param ezcli.Positional positional:
        :param int position:
        """
        self.positional = positional
        self.position: int = position
        self.message = f'Missing {position+1}. argument!'

