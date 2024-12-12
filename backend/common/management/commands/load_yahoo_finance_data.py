from django.core.management.base import BaseCommand
from currencies.models import CurrencyPair, ExchangeRate
from django.utils import timezone

from currencies.yahoo import fetch_exchange_rate


class Command(BaseCommand):
    """Django command to load Yahoo Finance data into the database for currency pairs"""

    def handle(self, *args, **options):
        self.stdout.write('Loading Yahoo Finance data to the database...')

        currency_pairs = CurrencyPair.objects.all()

        for currency_pair in currency_pairs:
            try:
                if exchange_rate := fetch_exchange_rate(currency_pair):
                    ExchangeRate.objects.create(
                        currency_pair=currency_pair,
                        exchange_rate=exchange_rate,
                        timestamp=timezone.now()
                    )
                    self.stdout.write(self.style.SUCCESS(f'Successfully created exchange_rate for {currency_pair} at {exchange_rate}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to fetch exchange rate for {currency_pair}. {e}'))

        self.stdout.write(self.style.SUCCESS('Data loaded successfully!'))
