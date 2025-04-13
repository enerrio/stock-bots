import datetime

from bot.domestic import post


def dummy_get_ticker_data(ticker_symbols: list[str]) -> dict[str, dict[str, float]]:
    # Return dummy ticker data similar to what yf.Tickers would return
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
        # Return a dummy object with a to_tz method that returns an object with py_datetime
        class DummyTZ:
            def to_tz(self, tz):
                return self

            def py_datetime(self):
                return datetime.datetime(2025, 4, 9, 13, 45)  # Fixed datetime: 1:45 PM

        return DummyTZ()


# Test when DEBUG mode is enabled: run() should not call the post method and return True
def test_run_debug(monkeypatch):
    # Set DEBUG to True in the post module
    monkeypatch.setattr(post, "DEBUG", True)
    # Override get_ticker_data to return dummy data
    monkeypatch.setattr(post, "get_ticker_data", dummy_get_ticker_data)
    # Override Instant to return a fixed datetime
    monkeypatch.setattr(post, "Instant", DummyInstant)
    # Patch login to simulate a successful login
    monkeypatch.setattr(
        post.BlueskyClient, "login", lambda self, username, password: "fake_session"
    )

    result = post.run()
    assert result is True


# Test when login fails: run() should return False immediately
def test_run_login_failure(monkeypatch):
    # Set DEBUG to True so that post is not invoked
    monkeypatch.setattr(post, "DEBUG", True)
    # Patch login to simulate a failed login (None)
    monkeypatch.setattr(
        post.BlueskyClient, "login", lambda self, username, password: None
    )

    result = post.run()
    assert result is False


# Test in production mode (DEBUG disabled) where post is successful
def test_run_production_success(monkeypatch):
    # Set DEBUG to False so that the post is attempted
    monkeypatch.setattr(post, "DEBUG", False)
    # Override get_ticker_data to return dummy data
    monkeypatch.setattr(post, "get_ticker_data", dummy_get_ticker_data)
    # Override Instant to return a fixed datetime
    monkeypatch.setattr(post, "Instant", DummyInstant)
    # Simulate successful login
    monkeypatch.setattr(
        post.BlueskyClient, "login", lambda self, username, password: "fake_session"
    )
    # Simulate successful post by returning a fake response
    monkeypatch.setattr(post.BlueskyClient, "post", lambda self, text: "fake_response")

    result = post.run()
    assert result is True


# Test in production mode (DEBUG disabled) where post fails
def test_run_production_failure(monkeypatch):
    # Set DEBUG to False so that the post is attempted
    monkeypatch.setattr(post, "DEBUG", False)
    # Override get_ticker_data to return dummy data
    monkeypatch.setattr(post, "get_ticker_data", dummy_get_ticker_data)
    # Override Instant to return a fixed datetime
    monkeyatch = monkeypatch.setattr  # alias for brevity
    monkeyatch(post, "Instant", DummyInstant)
    # Simulate successful login
    monkeypatch.setattr(
        post.BlueskyClient, "login", lambda self, username, password: "fake_session"
    )
    # Simulate failed post by returning None
    monkeypatch.setattr(post.BlueskyClient, "post", lambda self, text: None)

    result = post.run()
    assert result is False
