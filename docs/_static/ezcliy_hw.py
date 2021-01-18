from ezcliy import Command, KeyVal, Positional


class Hello(Command):
    count = KeyVal('--count', default=1)
    count.description = 'Number of greetings.'
    hello_name = Positional('name', ask_if_missing='naem?')
    hello_name.description = 'The person to greet.'

    def invoke(self):
        for _ in range(int(self.count)):
            print(f'Hello, {self.hello_name}!')


if __name__ == '__main__':
    Hello().cli_entry()
