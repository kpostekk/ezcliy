from ezcliy import *


class Parent(Command):
    a = Flag('-a')

    class ChildA(Command):
        name = 'cha'  # Subcommands must have names
        a: Flag  # That will got "a" param from parent

        def invoke(self):
            print(f'My name is {self.name} and my parent gave me param {self.a}')

    class CardiB(Command):
        name = 'cab'
        b = Flag('-b')

        class Kanye(Command):  # No level limits
            name = 'kanye'
            c = Flag('-c')

            def invoke(self):
                print('oh kanye')

        def invoke(self):
            print(f'I don\'t have my parent\'s param so i referenced my own {self.b}')

    def invoke(self):
        print('even, still i have children, i can be invoked')
        if not self.is_subcommand_issued:
            print('as we can see, i\'m still worthy')


if __name__ == '__main__':
    Parent().cli_entry()
