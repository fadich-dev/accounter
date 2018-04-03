from abc import ABCMeta, abstractmethod
from ..base import BaseCmdApp
from terminaltables import AsciiTable


class BaseCrudApp(BaseCmdApp, metaclass=ABCMeta):
    model_class = None
    name_single = None
    name_plural = None

    def __init__(self, args=''):
        super().__init__()
        self.name_single = self.name_single or self.model_class.__name__.lower()
        self.name_plural = self.name_plural or '{}s'.format(self.model_class.__name__.lower())

        self.prompt = '{} > '.format(self.name_plural.title())

        if args:
            self.onecmd(args)

    def do_list(self, args):
        """ List all items """

        if not self.model_class.objects.count():
            self.writeln('There are no {} yet'.format(self.name_plural.lower()))
            return

        table = AsciiTable(self.get_table_data())
        self.writeln(table.table)

    def get_table_data(self):
        return self.model_class.objects.values_list().all()

    @abstractmethod
    def do_add(self, args):
        pass

    @abstractmethod
    def do_edit(self, args):
        pass

    @abstractmethod
    def do_remove(self, args):
        pass
