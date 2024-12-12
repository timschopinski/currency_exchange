from django.db import models


class Currency(models.Model):
    ticker = models.CharField(max_length=3, unique=True)

    class Meta:
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.ticker


class CurrencyPair(models.Model):
    base_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='base_currency_pairs',
    )
    quote_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='quote_currency_pairs',
    )

    class Meta:
        unique_together = ('base_currency', 'quote_currency')

    def __str__(self):
        return f'{self.base_currency.ticker}{self.quote_currency.ticker}'


class ExchangeRate(models.Model):
    currency_pair = models.ForeignKey(
        CurrencyPair,
        on_delete=models.CASCADE,
        related_name='exchange_rates',
    )
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Exchange Rate'
        verbose_name_plural = 'Exchange Rates'

    def __str__(self):
        return f'{self.currency_pair} - {self.exchange_rate} at {self.timestamp}'
