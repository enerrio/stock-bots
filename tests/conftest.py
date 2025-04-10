import pytest


@pytest.fixture(autouse=True)
def set_test_env(monkeypatch):
    monkeypatch.setenv("BLUESKY_HANDLE", "test_handle")
    monkeypatch.setenv("BLUESKY_PASSWORD", "test_password")
    monkeypatch.setenv("DEBUG", "true")
