from .base import BaseCrudApp
from .mixins import NamedModelMixin
from backend.models import Account, Transaction, Currency


class CurrenciesCrud(BaseCrudApp):
    model_class = Currency
    name_single = 'currency'
    name_plural = 'currencies'

    def do_add(self, args):
        """ Create new currency """
        self.create()

    def do_edit(self, args):
        pass

    def do_remove(self, args):
        """ Remove currency """
        self.find(args).delete()

    def get_table_data(self):
        data = [['No', 'Abbreviation', 'Symbol', 'Extra']]
        data += [[a.id, a.abbreviation, a.symbol, a.extra] for a in self.model_class.objects.all()]

        return data

    def create(self):
        abbreviation = self.readln('Abbreviation: ')
        symbol = self.readln('Symbol: ')
        extra = self.readln('Extra: ')

        return self.model_class.objects.create(
            abbreviation=abbreviation,
            symbol=symbol,
            extra=extra
        )

    def find(self, key):
        if len(key) == 1:
            return self.model_class.objects.filter(id=key) or self.model_class.objects.filter(symbol=key)
        elif len(key) == 3:
            return self.model_class.objects.filter(abbreviation=key)

        return None


class AccountsCrud(BaseCrudApp, NamedModelMixin):
    model_class = Account

    def do_add(self, args):
        """ Create new account """
        self.create()

    def do_edit(self, args):
        pass

    def do_remove(self, args):
        """ Remove account """
        self.find(args).delete()

    def get_table_data(self):
        data = [['No', 'Name', 'Amount']]
        data += [[a.id, a.name, '{}{}'.format(a.currency.symbol, a.total)] for a in self.model_class.objects.all()]

        return data

    def create(self, extend_list=True):
        name = self.readln('Name: ')

        if extend_list:
            CurrenciesCrud().do_list('')

        _currency = self.readln('Currency: ')

        currency = CurrenciesCrud().find(_currency).first()
        if not currency:
            self.writeln('Currency not found. Create new currency:')
            currency = CurrenciesCrud().create()

        return self.model_class.objects.create(name=name, currency=currency)


class TransactionsCrud(BaseCrudApp, NamedModelMixin):
    model_class = Transaction

    def do_add(self, args):
        """ Create new transaction """
        self.create()

    def do_edit(self, args):
        pass

    def do_remove(self, args):
        """ Remove transaction """
        self.find(args).delete()

    def get_table_data(self):
        data = [['No', 'Name', 'Currency', 'Total']]
        for a in self.model_class.objects.order_by('-created_at').all():
            data.append([
                a.id,
                a.account,
                abs(a.value),
                ('income', 'consumption')[a.value < 0.0],
                a.comment,
                a.created_at.strftime('%d %b %Y at %H:%M:%S'),
            ])


        return data

    def create(self, extend_list=True):
        if extend_list:
            AccountsCrud().do_list('')

        account = AccountsCrud().find(self.readln('Choose account: ')).first()

        if not account:
            self.writeln('Account not found.')
            return self.create(False)

        action = None
        while action not in ['1', '2']:
            action = self.readln('Choose action:\n (1) - income\n (2) - consumption\n >> ')

        value = None
        while not value:
            try:
                value = float(self.readln('Amount: '))
            except ValueError as e:
                self.readln('The value should be float type')

        if action == '2':
            value *= -1

        comment = self.readln('Comment: ')

        return self.model_class.objects.create(account=account, value=value, comment=comment)
