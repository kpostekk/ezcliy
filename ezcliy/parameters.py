import re


class Parameter:
    value: str = None
    description: str = None

    def pass_args(self, user_args: list[str]) -> list[str]:
        """

        :param user_args: list of args to process
        :return: processed list of args, usally smaller then input
        """
        ...

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __bool__(self):
        return bool(self.value)


class Flag(Parameter):
    value: bool = False

    def __init__(self, *aliases: str):
        """

        :param aliases: must contains dash or dashes
        """
        self.aliases = aliases

    def pass_args(self, user_args: list[str]) -> list[str]:
        shrinked_args = [arg for arg in user_args if arg not in self.aliases]
        # noinspection PyTypeChecker
        self.value = len(shrinked_args) != len(user_args)
        return shrinked_args

    def __repr__(self):
        return f'<Flag {" ".join(self.aliases)} has value {self.value}>'


class KeyVal(Parameter):
    values: list[str] = []

    def __init__(self, keyname: str, default=None):
        """

        :param keyname: must contains dash or dashes
        """
        self.key = keyname
        if default is not None:
            self.values = [default]

    @property
    def value(self):
        try:
            return self.values[0]
        except IndexError:
            return None

    def pass_args(self, user_args: list[str]) -> list[str]:
        regex_rule = r'{}[=|\ ]\"?([^-][\w.,]*)\"?'.format(self.key)
        regex_match = re.findall(regex_rule, ' '.join(user_args))

        if not regex_match:
            return user_args

        self.values = list(regex_match)

        # Remove acquired values
        remove_tag = '<removeremoveremove>'
        h = user_args.copy()
        for i, arg in enumerate(h.copy()):
            if arg == self.key:
                h[i] = remove_tag
                continue
            h[i] = re.sub(regex_rule, remove_tag, arg)
        for i, arg in enumerate(h.copy()):
            if i > 0:
                if arg in self.values and h[i-1] == remove_tag:
                    h[i] = remove_tag
        h = [k for k in h if k != remove_tag]

        return h

    def __repr__(self):
        return f'<Value of {self.key} has value {self.value}>'
