from django.db import models
from django.db.models import Sum


class Currency(models.Model):
    abbreviation = models.CharField(max_length=3, unique=True)
    symbol = models.CharField(max_length=1, unique=True)
    extra = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return '{a}, {s}'.format(a=self.abbreviation, s=self.symbol)


class Account(models.Model):
    name = models.CharField(max_length=64, unique=True)
    currency = models.ForeignKey(Currency)

    @property
    def total(self):
        _sum = self.transaction_set.filter(account=self).aggregate(Sum('value'))['value__sum']
        return _sum or 0.0

    def __str__(self):
        return '{n}'.format(n=self.name)


class Transaction(models.Model):
    value = models.FloatField()
    account = models.ForeignKey(Account)
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{c}{v}, {a}'.format(c=self.account.currency.symbol, v=self.value, a=self.account)
