from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from currencies.factories import CurrencyFactory, CurrencyPairFactory, ExchangeRateFactory


class TestCurrencyListView(APITestCase):
    def test_currency_list_empty(self):
        url = reverse('currency')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_currency_list_with_data(self):
        CurrencyFactory.create_batch(3)

        url = reverse('currency')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertTrue(all('ticker' in currency for currency in response.data))


class TestCurrencyExchangeRateView(APITestCase):
    def test_exchange_rate_not_found(self):
        base_currency = CurrencyFactory(ticker='USD')
        quote_currency = CurrencyFactory(ticker='EUR')
        CurrencyPairFactory(base_currency=base_currency, quote_currency=quote_currency)

        url = reverse('exchange-rate', args=['USD', 'EUR'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'No exchange rate found for this currency pair.')

    def test_currency_pair_not_found(self):
        CurrencyFactory(ticker='USD')
        CurrencyFactory(ticker='EUR')

        url = reverse('exchange-rate', args=['USD', 'EUR'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_exchange_rate_success(self):
        base_currency = CurrencyFactory(ticker='USD')
        quote_currency = CurrencyFactory(ticker='EUR')
        currency_pair = CurrencyPairFactory(base_currency=base_currency, quote_currency=quote_currency)

        ExchangeRateFactory.create_batch(2, currency_pair=currency_pair)
        latest_rate = ExchangeRateFactory(currency_pair=currency_pair)

        url = reverse('exchange-rate', args=['USD', 'EUR'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['currency_pair'], f'{base_currency.ticker}{quote_currency.ticker}')
        self.assertEqual(response.data['exchange_rate'], str(latest_rate.exchange_rate))
        self.assertIn('timestamp', response.data)
