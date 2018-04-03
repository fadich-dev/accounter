import os
import cmd


class BaseCmdApp(cmd.Cmd):

    @staticmethod
    def clear():
        os.system('clear')

    def default(self, line):
        self.writeln('Unknown command {}. Use "help" for hint'.format(line))

    def writeln(self, msg=''):
        self.stdout.write('{}\n'.format(msg))

    def readln(self, prompt=''):

        return input(prompt).strip()

    def do_exit(self, args):
        """ Exit the program """

        return True
