import sys
from functools import cache
from typing import Optional

from ezcliy.arguements import Argument


class Command:
    name: Optional[str]
    description: Optional[str]
    values: list[str] = []
    legacy: dict[str, Argument] = {}

    @property
    @cache
    def commands(self) -> dict[str, type]:
        cmds = dict()
        for pair in [{o().name: o} for o in self.__class__.__dict__.values() if isinstance(o, type) if
                     issubclass(o, Command)]:
            cmds.update(pair)
        return cmds

    @property
    @cache
    def arguments(self) -> dict[str, Argument]:
        arg_fields = dict()
        for field in [{o: self.__class__.__dict__.get(o)} for o in self.__class__.__dict__ if
                      isinstance(self.__class__.__dict__.get(o), Argument)]:
            arg_fields.update(field)
        return arg_fields

    def dispatch(self, args: list[str]):
        # Loading legacy arguments
        for n in [name for name, t in self.__annotations__.items() if isinstance(t, type) if issubclass(t, Argument)]:
            if n in self.legacy:
                self.__setattr__(n, self.legacy.get(n))

        # Shrink requested arguments
        for arguments, name in [(self.arguments.get(a), a) for a in self.arguments]:
            args = arguments.pass_args(args)

        # Saved shrinked args
        self.values = [arg for arg in args if not arg.startswith('-')]

        # Check is first arg an command
        if len(self.values) > 0:
            if self.values[0] in self.commands.keys():
                # Shrink values
                cmd_name, self.values = self.values[0], self.values[1:]
                # Invoke, has args, first is subcommand
                self.invoke()
                # Prepare subcommand
                cmd: Command = self.commands.get(cmd_name)()
                cmd.legacy = self.arguments  # Passing aquired flags
                cmd.dispatch(args[args.index(cmd_name) + 1:])  # Passing only args after command
            else:
                self.invoke()  # Has args, first isn't subcommand
        else:
            self.invoke()  # Has no args

    # Invocation
    def invoke(self):
        ...

    # Entry points
    def cli_entry(self):
        self.dispatch(sys.argv[1:])

    def local_entry(self, *args: str):  # Only for dev purposes
        # noinspection PyTypeChecker
        self.dispatch(args)
