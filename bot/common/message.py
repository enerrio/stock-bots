from whenever import Instant


def build_market_update_message(ticker_data: dict, prefix: str = "$") -> str:
    current_time = Instant.now().to_tz("America/New_York").py_datetime()
    current_time_str = current_time.strftime("%I:%M %p ET").lstrip("0")
    message = f"🕰️ Market Update - {current_time_str}\n\n"
    for ticker, data in ticker_data.items():
        price = data.get("regularMarketPrice")
        previous = data.get("previousClose")
        change_percent = data.get("regularMarketChangePercent")
        if price is not None and previous is not None and change_percent is not None:
            emoji = "🟢" if price > previous else "🔴"
            message += (
                f"{emoji} {ticker} - {prefix}{price:,.2f} ({change_percent:+.2f}%)\n"
            )
        else:
            message += f"⚪ {ticker} - Data N/A\n"
    return message
