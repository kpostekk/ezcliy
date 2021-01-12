import re
from typing import Optional, Iterable, Sized


class Argument:
    value: object

    def pass_args(self, user_args: Iterable[str]) -> Iterable[str]: ...

    def __str__(self):
        return str(self.value)


class Flag(Argument):
    value: bool

    def __init__(self, *aliases: str):
        self.aliases = aliases

    def pass_args(self, user_args: Iterable[str]) -> Iterable[str]:
        shrinked_args = [arg for arg in user_args if arg not in self.aliases]
        # noinspection PyTypeChecker
        self.value = len(shrinked_args) != len(user_args)
        return shrinked_args

    def __bool__(self):
        return self.value


class KeyVal(Argument):
    pass
