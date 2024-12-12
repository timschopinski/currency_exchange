from django.core.management.base import BaseCommand
from currencies.models import CurrencyPair, ExchangeRate
import yfinance as yf
from decimal import Decimal
from django.utils import timezone


class Command(BaseCommand):
    """Django command to load Yahoo Finance data into the database for currency pairs"""

    def fetch_exchange_rate(self, currency_pair):
        ticker = f'{currency_pair.base_currency.ticker}{currency_pair.quote_currency.ticker}=X'
        try:
            data = yf.Ticker(ticker)
            exchange_rate = data.history(period='1d')['Close'][0]
            return Decimal(exchange_rate)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error fetching data for {ticker}: {e}'))
            return None

    def handle(self, *args, **options):
        self.stdout.write('Loading Yahoo Finance data to the database...')

        currency_pairs = CurrencyPair.objects.all()

        for currency_pair in currency_pairs:
            exchange_rate = self.fetch_exchange_rate(currency_pair)

            if exchange_rate is not None:
                ExchangeRate.objects.create(
                    currency_pair=currency_pair,
                    exchange_rate=exchange_rate,
                    timestamp=timezone.now()
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created exchange_rate for {currency_pair} at {exchange_rate}'))

            else:
                self.stdout.write(self.style.ERROR(f'Failed to fetch exchange rate for {currency_pair}.'))

        self.stdout.write(self.style.SUCCESS('Data loaded successfully!'))
