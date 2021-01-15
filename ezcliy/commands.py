import sys
from functools import cache
from typing import Optional

from ezcliy.parameters import Parameter
from ezcliy.positional import Positional


class Command:
    name: Optional[str]
    description: Optional[str]
    values: list[str] = []
    legacy: dict[str, Parameter] = {}

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
    def parameters(self) -> dict[str, Parameter]:
        params_fields = dict()
        for param_fields in [{o: self.__class__.__dict__.get(o)} for o in self.__class__.__dict__ if
                             isinstance(self.__class__.__dict__.get(o), Parameter)]:
            params_fields.update(param_fields)
        return params_fields

    @property
    @cache
    def positionals(self):
        return [p for p in self.__class__.__dict__.values() if isinstance(p, Positional)]

    def dispatch(self, args: list[str]):
        # Loading predecessor's parameters
        for n in [name for name, t in self.__annotations__.items() if isinstance(t, type) if issubclass(t, Parameter)]:
            if n in self.legacy:
                self.__setattr__(n, self.legacy.get(n))

        # Shrink requested parameters
        for arguments, name in [(self.parameters.get(a), a) for a in self.parameters]:
            args = arguments.pass_args(args)

        # Save cleaned values
        self.values = [arg for arg in args if not arg.startswith('-')]

        def pass_values_to_positionals():
            for i, p in enumerate(self.positionals):
                p.pass_values(self.values, i)

        # Check is first arg an command
        if len(self.values) > 0:
            if self.values[0] in self.commands.keys():
                # Shrink values
                cmd_name, self.values = self.values[0], self.values[1:]
                # Invoke, has args, first is subcommand
                self.invoke()
                # Prepare subcommand
                cmd: Command = self.commands.get(cmd_name)()
                cmd.legacy = self.parameters  # Passing aquired flags
                cmd.dispatch(args[args.index(cmd_name) + 1:])  # Passing only args after command
            else:
                pass_values_to_positionals()
                self.invoke()  # Has args, first isn't subcommand
        else:
            pass_values_to_positionals()  # This should raise an error
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
