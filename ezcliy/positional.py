from typing import Optional
from ezcliy.exceptions import MissingPositional


class Positional:
    value: str = None

    def __init__(self, name: str, ask_if_missing: Optional[str] = None, optional=False):
        self.name = name
        self.ask_if_missing = ask_if_missing
        self.optional = optional

    def pass_values(self, values: list[str], position: int):
        try:
            self.value = values[position]
        except IndexError as ie:
            if self.ask_if_missing:
                self.value = input(self.ask_if_missing + ": ").strip()
            elif self.optional:
                pass
            else:
                raise MissingPositional(self, position)

    def __repr__(self):
        return f'<Positional expecting {self.name}>'

    def __str__(self):
        return self.value
