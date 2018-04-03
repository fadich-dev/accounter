from .base import BaseCmdApp
from .crud import models


class Application(BaseCmdApp):

    def __init__(self):
        super().__init__()
        self.prompt = '> '
        self.doc_header = 'Available commands (for hint on a specific command, type "help _command_")'

    def do_accounts(self, args):
        """ Manage your accounts """

        try:
            models.AccountsCrud(args).cmdloop()
        except KeyboardInterrupt:
            self.writeln()

    def do_currencies(self, args):
        """ Manage your currencies """

        try:
            models.CurrenciesCrud(args).cmdloop()
        except KeyboardInterrupt:
            self.writeln()

    def do_transactions(self, args):
        """ Manage your transactions """

        try:
            models.TransactionsCrud(args).cmdloop()
        except KeyboardInterrupt:
            self.writeln()
