import yfinance as yf
from currencies.models import CurrencyPair
from decimal import Decimal


def fetch_exchange_rate(currency_pair: CurrencyPair) -> Decimal:
    ticker = f'{currency_pair.base_currency.ticker}{currency_pair.quote_currency.ticker}=X'
    data = yf.Ticker(ticker)
    exchange_rate = data.history(period='1d')['Close'][0]

    return Decimal(exchange_rate)
