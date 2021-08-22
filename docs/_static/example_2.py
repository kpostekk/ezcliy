import math

from ezcliy import Command, Positional, Flag


class QMath(Command):
    name = 'qmath.py'
    none_args_will_not_trigger_help = False

    floor = Flag('-f', '--floor')
    ceil = Flag('-c', '--ceil')

    class Sum(Command):
        description = 'Sums all passed values.'
        floor: Flag  # Reuse parent's parameters
        ceil: Flag

        def invoke(self):
            result = sum(map(lambda v: float(v), self.values))
            if self.floor.value:
                print(math.floor(result))
            elif self.ceil.value:
                print(math.ceil(result))
            else:
                print(result)

    class Product(Command):
        description = 'Product of all passed values.'

        def invoke(self):
            print(math.prod(map(lambda v: float(v), self.values)))

    class Root(Command):
        x = Positional('x')
        n = Positional('n')
        require_all_defined_positionals = True

        def invoke(self):
            print(float(self.x.value) ** 1 / float(self.n.value))


if __name__ == '__main__':
    QMath().cli_entry()
