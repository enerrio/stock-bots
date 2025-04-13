import yfinance as yf

from bot.common.fetch_data import get_ticker_data


# Dummy classes to simulate yfinance ticker behavior
class DummyTicker:
    def __init__(self, info):
        self.info = info


class DummyTickers:
    def __init__(self, symbols):
        self.tickers = {
            symbol: DummyTicker(
                {
                    "previousClose": 100.0,
                    "open": 101.0,
                    "regularMarketPrice": 102.0,
                    "regularMarketChangePercent": 2.0,
                    "regularMarketChange": 2.0,
                }
            )
            for symbol in symbols
        }


def test_get_ticker_data(monkeypatch):
    # Define test index symbols
    test_symbols = ["TEST1", "TEST2"]

    # Override INDEX_SYMBOLS in bot.fetch_data with the test symbols
    # monkeypatch.setattr("bot.common.fetch_data.INDEX_SYMBOLS", test_symbols)

    # Monkeypatch yfinance.Tickers to return our dummy data
    monkeypatch.setattr(yf, "Tickers", lambda symbols: DummyTickers(symbols))

    # Call the function under test
    ticker_data = get_ticker_data(test_symbols)

    # Assert that the returned data is structured correctly
    assert isinstance(ticker_data, dict)
    assert set(ticker_data.keys()) == set(test_symbols)

    for symbol in test_symbols:
        data = ticker_data[symbol]
        assert data["previousClose"] == 100.0
        assert data["open"] == 101.0
        assert data["regularMarketPrice"] == 102.0
        assert data["regularMarketChangePercent"] == 2.0
        assert data["regularMarketChange"] == 2.0
