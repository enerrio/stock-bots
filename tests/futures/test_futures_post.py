import datetime

from bot.futures import post


def dummy_get_ticker_data(ticker_symbols: list[str]) -> dict[str, dict[str, float]]:
    return {
        symbol: {
            "regularMarketPrice": 105.25,
            "previousClose": 104.50,
            "regularMarketChangePercent": 0.72,
        }
        for symbol in ticker_symbols
    }


class DummyInstantOpen:
    @staticmethod
    def now():
        # Simulate a time when the futures market is open (e.g., Sunday at 6:00 PM CT)
        class DummyTZ:
            def to_tz(self, tz: str):
                return self

            def py_datetime(self):
                return datetime.datetime(2025, 4, 13, 18, 0)  # Sunday, 6:00 PM CT

        return DummyTZ()


class DummyInstantClosed:
    @staticmethod
    def now():
        # Simulate a time when the futures market is closed (e.g., Sunday at 4:00 PM CT)
        class DummyTZ:
            def to_tz(self, tz: str):
                return self

            def py_datetime(self):
                return datetime.datetime(2025, 4, 13, 16, 0)  # Sunday, 4:00 PM CT

        return DummyTZ()


# Test when DEBUG mode is enabled: run() should not call the post method.
def test_run_debug(monkeypatch):
    monkeypatch.setattr(post, "DEBUG", True)
    monkeypatch.setattr(post, "get_ticker_data", dummy_get_ticker_data)
    monkeypatch.setattr(post, "Instant", DummyInstantOpen)
    monkeypatch.setattr(
        post.BlueskyClient, "login", lambda self, username, password: "fake_session"
    )
    result = post.run()
    assert result is True


# Test when login fails: run() should return False immediately.
def test_run_login_failure(monkeypatch):
    monkeypatch.setattr(post, "DEBUG", True)
    monkeypatch.setattr(post, "Instant", DummyInstantOpen)
    monkeypatch.setattr(
        post.BlueskyClient, "login", lambda self, username, password: None
    )
    result = post.run()
    assert result is False


# Test in production mode (DEBUG disabled) where post is successful.
def test_run_production_success(monkeypatch):
    monkeypatch.setattr(post, "DEBUG", False)
    monkeypatch.setattr(post, "get_ticker_data", dummy_get_ticker_data)
    # Use DummyInstantOpen to simulate that the market is open.
    monkeypatch.setattr(post, "Instant", DummyInstantOpen)
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
    monkeypatch.setattr(post, "Instant", DummyInstantOpen)
    monkeypatch.setattr(
        post.BlueskyClient, "login", lambda self, username, password: "fake_session"
    )
    monkeypatch.setattr(post.BlueskyClient, "post", lambda self, text: None)
    result = post.run()
    assert result is False


# Test that the futures bot exits early if the market is closed.
def test_market_closed(monkeypatch):
    # Simulate the market being closed (e.g., Sunday before 5:00 PM CT).
    monkeypatch.setattr(post, "DEBUG", False)
    monkeypatch.setattr(post, "get_ticker_data", dummy_get_ticker_data)
    monkeypatch.setattr(post, "Instant", DummyInstantClosed)
    # Patch the BlueskyClient.login (it won't be used because the function should exit before that)
    monkeypatch.setattr(
        post,
        "BlueskyClient",
        type(
            "DummyClient", (), {"login": lambda self, username, password: "irrelevant"}
        ),
    )
    result = post.run()
    # When the market is closed, run() logs the condition and returns True without posting.
    assert result is True
