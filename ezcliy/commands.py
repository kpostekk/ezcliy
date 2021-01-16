import sys
from functools import cache
from typing import Optional

import colorama
import yaml

from ezcliy.parameters import Parameter
from ezcliy.positional import Positional
from ezcliy.exceptions import MessageableException, TooManyValues
from ezcliy.helpman import Helpman


class Command:
    """
    Base class for creating commands. You probably will override this class
    """
    name: Optional[str]
    description: Optional[str]
    values: list[str] = []
    legacy: dict[str, Parameter] = {}
    only_positionals = False
    help: Helpman = Helpman()

    @property
    @cache
    def commands(self) -> dict[str, type]:
        """

        :return: Children...
        """
        cmds = dict()
        for pair in [{o().name: o} for o in self.__class__.__dict__.values() if isinstance(o, type) if
                     issubclass(o, Command)]:
            cmds.update(pair)
        return cmds

    @property
    @cache
    def parameters(self) -> dict[str, Parameter]:
        """

        :return: All declared parameters as name-class dict
        """
        parameters = {'help': self.help}
        for name, param in [(n, p) for n, p in self.__class__.__dict__.items() if isinstance(p, Parameter)]:
            parameters.update({name: param})
        return parameters

    @property
    @cache
    def positionals(self):
        """

        :return: All declared positionals
        """
        return [p for p in self.__class__.__dict__.values() if isinstance(p, Positional)]

    def __help_check(self):
        if self.help:
            self.help.render_help(self)

    def dispatch(self, args: list[str]):
        """

        :param args: list of arguments to process
        :return: processed list of arguments
        """
        # Loading predecessor's parameters
        for n in [name for name, t in self.__annotations__.items() if isinstance(t, type) if issubclass(t, Parameter)]:
            if n in self.legacy:
                self.__setattr__(n, self.legacy.get(n))

        # Shrink requested parameters
        for arguments, name in [(self.parameters.get(a), a) for a in self.parameters]:
            args = arguments.pass_args(args)

        # Save cleaned values
        self.values = [arg for arg in args if not arg.startswith('-')]

        if len(self.values) != len(self.positionals) and self.only_positionals:
            raise TooManyValues(self.values, len(self.positionals))

        def pass_values_to_positionals():
            for i, p in enumerate(self.positionals):
                p.pass_values(self.values, i)

        # Check is first arg an command
        if len(self.values) > 0:
            if self.values[0] in self.commands.keys():
                # Shrink values
                cmd_name, self.values = self.values[0], self.values[1:]
                # Invoke, has args, first is subcommand
                if not self.help:
                    self.invoke()
                # Prepare subcommand
                cmd: Command = self.commands.get(cmd_name)()
                cmd.legacy = self.parameters.copy()  # Passing aquired flags
                cmd.dispatch(args[args.index(cmd_name) + 1:])  # Passing only args after command
            else:
                self.__help_check()
                pass_values_to_positionals()
                self.invoke()  # Has args, first isn't subcommand
        else:
            self.__help_check()
            pass_values_to_positionals()  # This should raise an error
            self.invoke()  # Has no args

    # Invocation
    def invoke(self):
        """
        The entry point for your command.
        """
        ...

    # Entry points
    def entry(self, *args: str):
        try:
            self.dispatch(list(args))
        except MessageableException as mex:
            print(colorama.Fore.RED +
                  yaml.safe_dump({
                      'error': mex.__class__.__name__,
                      'message': mex.message
                  }) + colorama.Style.RESET_ALL
                  )

    def cli_entry(self):
        """
        This method grabs args from terminal. You should put it into ``if main``. This should be used in production.
        """
        self.entry(*sys.argv[1:])

    def local_entry(self, sim_input: str):  # Only for dev purposes
        self.entry(*sim_input.split(' '))
