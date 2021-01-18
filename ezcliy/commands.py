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
    name: str
    """Name of command."""

    description: str
    """Description for help"""

    values: list[str] = []
    """Cleaned values from cmd"""

    legacy: dict[str, Parameter] = {}
    """Parameters inherited after previous command"""

    restrict_to_positionals_only = False
    """If true, allow only values referenced as positionals"""

    allow_empty_calls = False
    """If true, will not print help when command is issued without parameters"""

    help: Helpman
    """Object that handles --help, it's just a powerful flag instance"""

    def __init__(self):
        self.name = self.__class__.__name__.lower()
        self.description = f'The is not description for {self.name}'
        self.help = Helpman()

    @property
    @cache
    def commands(self) -> dict[str, type]:
        """

        :return: Subcommands
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

        :return: All declared parameters as name-parameter dict
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
        :rtype: list[Positional]
        """
        return [p for p in self.__class__.__dict__.values() if isinstance(p, Positional)]

    def __help_check(self):
        if self.help:
            self.help.render_help(self)

        if len([p for p in self.positionals if p is not None]):
            return

    def __restriction_check(self):
        if len(self.values) != len(self.positionals) and self.restrict_to_positionals_only:
            raise TooManyValues(self.values, len(self.positionals))

    def dispatch(self, args: list[str]):
        """
        The magic spaghetti of framework.

        :param args: list of arguments to process
        """
        # Loading predecessor's parameters
        for n in [name for name, t in self.__annotations__.items() if isinstance(t, type) if issubclass(t, Parameter)]:
            if n in self.legacy:
                self.__setattr__(n, self.legacy.get(n))

        # Special help check
        if not len(args) and not self.allow_empty_calls:
            self.help.render_help(self)

        # Shrink requested parameters
        for argument, name in [(self.parameters.get(a), a) for a in self.parameters]:
            args = argument.pass_args(args)

        # Save cleaned values
        self.values = [arg for arg in args if not arg.startswith('-') and arg != '']

        def pass_values_to_positionals():
            for i, p in enumerate(self.positionals):
                p.pass_values(self.values, i)

        # Check is first arg an command
        if len(self.values) > 0:
            if self.values[0] in self.commands.keys():
                # Shrink values
                cmd_name, self.values = self.values[0], self.values[1:]
                # Checks
                self.__restriction_check()
                # Invoke, has args, first is subcommand
                if not self.help:
                    self.invoke()
                # Prepare subcommand
                cmd: Command = self.commands.get(cmd_name)()
                cmd.legacy = self.parameters.copy()  # Passing aquired flags
                cmd.dispatch(args[args.index(cmd_name) + 1:])  # Passing only args after command
            else:
                self.__help_check()
                self.__restriction_check()
                pass_values_to_positionals()
                self.invoke()  # Has args, first isn't subcommand
        else:
            self.__help_check()
            self.__restriction_check()
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
        """
        Handles errors caused by dispatch method. Used also for testing. Use it on dev env.

        :param str args:
        """
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
