import yfinance as yf


def get_ticker_data(index_symbols: list[str]) -> dict[str, dict[str, float]]:
    """Get ticker data from Yahoo Finance.

    Fetches current market data for tickers defined in index_symbols, including
    previous close price, open price, current market price, percentage change,
    and absolute change.

    Args:
        index_symbols (list[str]): List of ticker symbols to fetch data for.

    Returns:
        dict[str, dict[str, float]]: Ticker mapping symbols to dictionaries of market data.
    """
    tickers = yf.Tickers(index_symbols)
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
        for ticker in index_symbols
    }
    return ticker_info
