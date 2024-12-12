from rest_framework import serializers

from currencies.models import Currency, CurrencyPair, ExchangeRate


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ['id', 'ticker']
        read_only_fields = fields


class CurrencyPairSerializer(serializers.ModelSerializer):
    base_currency = CurrencySerializer()
    quote_currency = CurrencySerializer()

    class Meta:
        model = CurrencyPair
        fields = ['id', 'base_currency', 'quote_currency']
        read_only_fields = fields


class ExchangeRateSerializer(serializers.ModelSerializer):
    currency_pair = serializers.CharField()

    class Meta:
        model = ExchangeRate
        fields = ['id', 'currency_pair', 'exchange_rate', 'timestamp']
        read_only_fields = fields
