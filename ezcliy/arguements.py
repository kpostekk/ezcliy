import re


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
    value: str = None

    def __init__(self, keyname: str):
        self.key = keyname

    def pass_args(self, user_args: list[str]) -> list[str]:
        regex_rule = r'--{}[=|\ ]\"?([^-][\w.,]*)\"?'.format(self.key)
        regex_match = re.search(regex_rule, ' '.join(user_args))

        if regex_match is None:
            return user_args

        self.value = regex_match.groups()[0]
        kv_with_eq, kv_with_sp = f'--{self.key}={self.value}', f'--{self.key}'
        if kv_with_eq in user_args:
            user_args.remove(kv_with_eq)
        elif kv_with_sp in user_args:
            user_args.remove(kv_with_sp)
            user_args.remove(self.value)
        return user_args

    def __repr__(self):
        return f'<Value of {self.key} has value {self.value}>'
