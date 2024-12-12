from django.contrib import admin

from common.admin_mixins import ReadOnlyModelAdminMixin
from .models import Currency, CurrencyPair, ExchangeRate


@admin.register(Currency)
class CurrencyAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    list_display = ('ticker',)
    search_fields = ('ticker',)
    list_filter = ('ticker',)


@admin.register(CurrencyPair)
class CurrencyPairAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    list_display = ('base_currency', 'quote_currency')
    search_fields = ('base_currency__ticker', 'quote_currency__ticker')
    list_filter = ('base_currency', 'quote_currency')


@admin.register(ExchangeRate)
class ExchangeRateAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    list_display = ('currency_pair', 'exchange_rate', 'timestamp')
    search_fields = ('currency_pair__base_currency__ticker', 'currency_pair__quote_currency__ticker')
    list_filter = ('currency_pair', 'timestamp')
    readonly_fields = ('timestamp',)
