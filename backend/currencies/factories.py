import random

from django.utils import timezone
import factory
from decimal import Decimal

from common.factories import UniqueSequenceFactoryMixin
from currencies.models import Currency, CurrencyPair, ExchangeRate


class CurrencyFactory(UniqueSequenceFactoryMixin, factory.django.DjangoModelFactory):
    ticker = factory.Sequence(lambda n: f'CUR{n: 03}')

    class Meta:
        model = Currency


class CurrencyPairFactory(factory.django.DjangoModelFactory):
    base_currency = factory.SubFactory(CurrencyFactory)
    quote_currency = factory.SubFactory(CurrencyFactory)

    class Meta:
        model = CurrencyPair

    @factory.lazy_attribute
    def quote_currency(self):
        available_currencies = Currency.objects.exclude(id=self.base_currency.id)
        return random.choice(available_currencies)


class ExchangeRateFactory(factory.django.DjangoModelFactory):
    currency_pair = factory.SubFactory(CurrencyPairFactory)
    exchange_rate = factory.LazyAttribute(lambda _: Decimal(random.uniform(0, 5)).quantize(Decimal('0.0001')))
    timestamp = timezone.now()

    class Meta:
        model = ExchangeRate
