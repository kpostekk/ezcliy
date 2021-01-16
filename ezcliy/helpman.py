from ezcliy.parameters import Flag


class Helpman(Flag):
    def __init__(self):
        super().__init__('--help')

    def pass_args(self, user_args: list[str]) -> list[str]:
        if self.value:
            return user_args
        return super(Helpman, self).pass_args(user_args)

    @staticmethod
    def render_help(command):
        """

        :param ezcli.Command command:
        :return:
        """
        lines = []

        # Get commands
        if command.commands:
            lines.append('Commands:')
            for subcom in command.commands.values():
                lines.append(f'    {subcom().name} - {subcom().description}')
            lines.append('')

        # Get params
        if command.parameters:
            lines.append('Parameters:')
            for key, param in command.parameters.items():
                lines.append(f'    {" ".join(param.aliases)} - {param.aliases}')

        print(*lines, sep='\n')
        exit()
