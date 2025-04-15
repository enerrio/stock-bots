import datetime

from bot.international import post


def dummy_get_ticker_data(ticker_symbols: list[str]) -> dict[str, dict[str, float]]:
    # Return dummy ticker data similar to what yf.Tickers would return.
    return {
        symbol: {
            "regularMarketPrice": 105.25,
            "previousClose": 104.50,
            "regularMarketChangePercent": 0.72,
        }
        for symbol in ticker_symbols
    }


class DummyInstant:
    @staticmethod
    def now():
        # Fixed time: April 9, 2025, 1:45 PM in the specified timezone.
        class DummyTZ:
            def to_tz(self, tz: str):
                return self

            def py_datetime(self):
                return datetime.datetime(2025, 4, 9, 13, 45)

        return DummyTZ()


# Test when DEBUG mode is enabled: run() should not call the post method and return True.
def test_run_debug(monkeypatch):
    monkeypatch.setattr(post, "DEBUG", True)
    monkeypatch.setattr(post, "get_ticker_data", dummy_get_ticker_data)
    monkeypatch.setattr(
        post.BlueskyClient, "login", lambda self, username, password: "fake_session"
    )
    result = post.run()
    assert result is True


# Test when login fails: run() should return False immediately.
def test_run_login_failure(monkeypatch):
    monkeypatch.setattr(post, "DEBUG", True)
    monkeypatch.setattr(
        post.BlueskyClient, "login", lambda self, username, password: None
    )
    result = post.run()
    assert result is False


# Test in production mode (DEBUG disabled) where post is successful.
def test_run_production_success(monkeypatch):
    monkeypatch.setattr(post, "DEBUG", False)
    monkeypatch.setattr(post, "get_ticker_data", dummy_get_ticker_data)
    monkeypatch.setattr(
        post.BlueskyClient, "login", lambda self, username, password: "fake_session"
    )
    monkeypatch.setattr(post.BlueskyClient, "post", lambda self, text: "fake_response")
    result = post.run()
    assert result is True


# Test in production mode (DEBUG disabled) where post fails.
def test_run_production_failure(monkeypatch):
    monkeypatch.setattr(post, "DEBUG", False)
    monkeypatch.setattr(post, "get_ticker_data", dummy_get_ticker_data)
    monkeypatch.setattr(
        post.BlueskyClient, "login", lambda self, username, password: "fake_session"
    )
    monkeypatch.setattr(post.BlueskyClient, "post", lambda self, text: None)
    result = post.run()
    assert result is False
