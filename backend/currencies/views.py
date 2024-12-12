from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView, get_object_or_404
from rest_framework.response import Response

from currencies.models import Currency, CurrencyPair, ExchangeRate
from currencies.serializers import CurrencySerializer, ExchangeRateSerializer


class CurrencyListView(ListAPIView):
    serializer_class = CurrencySerializer

    def get_queryset(self):
        return Currency.objects.all()


class CurrencyExchangeRateView(GenericAPIView):
    @staticmethod
    def get_currency_pair(base_currency, quote_currency):
        base_currency = get_object_or_404(Currency, ticker=base_currency)
        quote_currency = get_object_or_404(Currency, ticker=quote_currency)
        return get_object_or_404(CurrencyPair, base_currency=base_currency, quote_currency=quote_currency)

    @staticmethod
    def get_latest_exchange_rate(currency_pair):
        return ExchangeRate.objects.filter(currency_pair=currency_pair).order_by('-timestamp').first()

    def get(self, request, base_currency, quote_currency):
        currency_pair = self.get_currency_pair(base_currency, quote_currency)
        exchange_rate = self.get_latest_exchange_rate(currency_pair)

        if not exchange_rate:
            return Response(
                {'detail': 'No exchange rate found for this currency pair.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ExchangeRateSerializer(exchange_rate)
        return Response(serializer.data, status=status.HTTP_200_OK)
