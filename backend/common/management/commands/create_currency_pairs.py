from django.core.management.base import BaseCommand
from currencies.models import Currency, CurrencyPair


class Command(BaseCommand):
    """Django command to create all possible currency pairs"""

    def create_currency_pair(self, base_currency, quote_currency):
        currency_pair, created = CurrencyPair.objects.get_or_create(
            base_currency=base_currency,
            quote_currency=quote_currency
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'CurrencyPair: {currency_pair} created.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'CurrencyPair: {currency_pair} already exists.'))

    def handle(self, *args, **options):
        self.stdout.write('Creating currency pairs...')

        currencies = Currency.objects.all()

        for base_currency in currencies:
            for quote_currency in currencies:
                if base_currency != quote_currency:
                    self.create_currency_pair(base_currency, quote_currency)

        self.stdout.write(self.style.SUCCESS('All possible currency pairs created.'))
