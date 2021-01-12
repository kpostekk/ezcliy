import re
import sys
from ezcliy.arguements import Flag, Argument
from typing import Optional, Iterable


class Command:
    name: Optional[str]
    description: Optional[str]
    values: list[str]

    # Get commands
    def get_commands_bindings(self) -> dict[str, type]:
        commands = []
        for name in dir(self):
            v = self.__getattribute__(name)
            if isinstance(v, type) and name != '__class__':
                if issubclass(v, Command):
                    commands.append(v)

        bindings = {}
        for command in commands:
            bindings.update({command().name: command})

        return bindings

    # Argument processing
    def push_args(self, user_args: list[str]):
        for attr in [self.__getattribute__(name) for name in dir(self)]:
            if isinstance(attr, Argument):
                user_args = attr.pass_args(user_args)

        self.values = user_args
        if len(self.values) > 0:
            if self.values[0] in self.get_commands_bindings().keys():
                cmd: Command = self.get_commands_bindings().get(self.values[0])()
                cmd.push_args(self.values[1:])

        self.invoke()

    # Invocation
    def invoke(self): ...

    # Entry points
    def cli_entry(self):
        self.push_args(sys.argv[1:])

    def local_entry(self, *args: str):
        # noinspection PyTypeChecker
        self.push_args(args)


if __name__ == '__main__':
    class Test(Command):
        class StringOps(Command):
            name = 'string'

            class StringUpper(Command):
                name = 'up'

                def invoke(self):
                    print(' '.join(self.values).upper())

    Test().local_entry('string', 'up', 'hdajsk', 'hdasjikdhasjk')
