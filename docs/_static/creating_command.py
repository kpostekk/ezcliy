from ezcliy import Command


class SmallTextProcessor(Command):
    def invoke(self):
        print(f'You have passed {len(self.values)} arguments!')


if __name__ == '__main__':
    SmallTextProcessor().cli_entry()
