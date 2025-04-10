import yfinance as yf

from config.settings import INDEX_SYMBOLS


def get_ticker_data() -> dict[str, dict[str, float]]:
    """Get ticker data from Yahoo Finance.

    Fetches current market data for tickers defined in INDEX_SYMBOLS, including
    previous close price, open price, current market price, percentage change,
    and absolute change.

    Returns:
        dict[str, dict[str, float]]: Ticker mapping symbols to dictionaries of market data.
    """
    tickers = yf.Tickers(INDEX_SYMBOLS)
    ticker_info = {
        ticker: {
            "previousClose": tickers.tickers[ticker].info["previousClose"],
            "open": tickers.tickers[ticker].info["open"],
            "regularMarketPrice": tickers.tickers[ticker].info["regularMarketPrice"],
            "regularMarketChangePercent": tickers.tickers[ticker].info[
                "regularMarketChangePercent"
            ],
            "regularMarketChange": tickers.tickers[ticker].info["regularMarketChange"],
        }
        for ticker in INDEX_SYMBOLS
    }
    return ticker_info
