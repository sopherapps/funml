"""Errors for this domain"""


class MatchError(BaseException):
    """Exception returned when a match fails to find an appropriate case for argument.

    Args:
        arg: the argument whose match was not found
    """

    def __init__(self, arg: str):
        self.arg = arg

    def __repr__(self):
        return f"MatchError: No match found for {self.arg}"
