from bot.common.message import build_market_update_message


def test_build_market_update_message():
    ticker_data = {
        "TEST": {
            "regularMarketPrice": 105.25,
            "previousClose": 104.50,
            "regularMarketChangePercent": 0.72,
        },
        "NODATA": {},
    }
    message = build_market_update_message(ticker_data, prefix="$")
    assert "TEST" in message
    assert "⚪ NODATA - Data N/A" in message
