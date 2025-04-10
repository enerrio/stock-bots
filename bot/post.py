import json
import logging
from typing import Any

from atproto import Client, models
from atproto.exceptions import AtProtocolError
from whenever import Instant

from bot.fetch_data import get_ticker_data
from config.settings import BLUESKY_HANDLE, BLUESKY_PASSWORD, DEBUG, INDEX_SYMBOLS

logger = logging.getLogger(__name__)


class BlueskyClient:
    """Bluesky client to handle logging in and posting."""

    def __init__(self) -> None:
        self.client = Client(base_url="https://bsky.social")

    def login(
        self, username: str, password: str
    ) -> models.AppBskyActorDefs.ProfileViewDetailed:
        """Login to Bluesky using username and password.

        Args:
            username (str): Bluesky username.
            password (str): Bluesky password.

        Returns:
            models.AppBskyActorDefs.ProfileViewDetailed: Bluesky session object.
            None: If login fails.
        """
        try:
            session = self.client.login(username, password)
            return session
        except AtProtocolError as err:
            logging.error("Bluesky login error: %s", err)
            return None

    def post(self, text: str) -> models.AppBskyFeedPost.CreateRecordResponse:
        """Post to Bluesky.

        Args:
            text (str): Content of the post.

        Returns:
            models.AppBskyFeedPost.CreateRecordResponse: Post response object.
        """
        try:
            post = self.client.send_post(text)
            return post
        except AtProtocolError as err:
            logging.error("Bluesky post error: %s", err)
            return None


def run() -> bool:
    """Main entrypoint for the script. Will gather ticker data and post to Bluesky.

    Returns:
        bool: Whether post was successful or not.
    """
    logger.info("Debug mode is %s", "enabled" if DEBUG else "disabled")
    logger.info("Setting up Bluesky client")
    client = BlueskyClient()
    session = client.login(BLUESKY_HANDLE, BLUESKY_PASSWORD)
    if not session:
        logging.error("Login failed. Exiting.")
        return False

    # Get ticker data from the fetch_data script
    logger.info("Fetching ticker data")
    ticker_data = get_ticker_data()
    current_time = Instant.now().to_tz("America/New_York").py_datetime()
    current_time_str = current_time.strftime("%I:%M %p ET").lstrip("0")

    message = f"🕰️ Market Update - {current_time_str}\n\n"
    for ticker in INDEX_SYMBOLS:
        data = ticker_data[ticker]
        price = data.get("regularMarketPrice")
        previous = data.get("previousClose")
        change_percent = data.get("regularMarketChangePercent")

        if price is not None and previous is not None and change_percent is not None:
            emoji = "🟢" if price > previous else "🔴"
            message += f"{emoji} {ticker} - ${price:.2f} ({change_percent:+.2f}%)\n"
        else:
            message += f"⚪ {ticker} - Data N/A\n"

    if not DEBUG:
        response = client.post(message)
        if response:
            logging.info("Post successful. Response: %s", response)
        else:
            logging.error("Failed to post update.")
            return False
    logging.info("Debug mode is enabled. No post will be made.")
    return True


def lambda_handler(event, context) -> dict[str, Any]:
    """Main entry point for AWS Lambda function.

    Args:
        event: Contains info about service invoking function.
        context: Contains methods + properties about invocation/runtime/function.

    Returns:
        dict[str, Any]: Dictionary containing lambda invocation response info.
    """
    result = run()
    if not result:
        return {"statusCode": 500, "body": json.dumps("Failed to post update")}
    return {"statusCode": 200, "body": json.dumps("Post successful")}
