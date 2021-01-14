import re
from typing import Optional, Iterable, Sized


class Argument:
    value: object = None

    def pass_args(self, user_args: list[str]) -> list[str]: ...

    def __str__(self):
        return str(self.value)


class Flag(Argument):
    value: bool = False

    def __init__(self, *aliases: str):
        self.aliases = aliases

    def pass_args(self, user_args: list[str]) -> list[str]:
        shrinked_args = [arg for arg in user_args if arg not in self.aliases]
        # noinspection PyTypeChecker
        self.value = len(shrinked_args) != len(user_args)
        return shrinked_args

    def __bool__(self):
        return self.value

    def __repr__(self):
        return f'<Flag {" ".join(self.aliases)} has value {self.value}>'

class KeyVal(Argument):
    pass
