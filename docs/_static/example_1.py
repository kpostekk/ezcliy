from ezcliy import Command, Positional


class Example(Command):
    number = Positional('the number to be squared')
    number.description = 'should be an int'
    require_all_defined_positionals = True

    def invoke(self):
        print(int(self.number) ** 2)


if __name__ == '__main__':
    Example().cli_entry()
