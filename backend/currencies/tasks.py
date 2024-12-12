import logging

from celery import shared_task
from django.utils import timezone

from currencies.models import ExchangeRate
from currencies.yahoo import fetch_exchange_rate
from currencies.models import CurrencyPair


@shared_task
def sync_exchange_rates_from_yahoo():
    logger = logging.getLogger('django')
    currency_pairs = CurrencyPair.objects.all()
    for currency_pair in currency_pairs:
        try:
            if exchange_rate := fetch_exchange_rate(currency_pair):
                ExchangeRate.objects.create(
                    currency_pair=currency_pair,
                    exchange_rate=exchange_rate,
                    timestamp=timezone.now()
                )
            logger.debug(f'Successfully created exchange_rate for {currency_pair} at {exchange_rate}')
        except Exception as e:
            logger.warning(f'Error fetching data for {currency_pair}: {e}')
