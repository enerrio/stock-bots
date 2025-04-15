import json
import logging
from typing import Any

from bot.common.client import BlueskyClient
from bot.common.fetch_data import get_ticker_data
from bot.common.message import build_market_update_message
from config.international.settings import (
    BLUESKY_HANDLE,
    BLUESKY_PASSWORD,
    DEBUG,
    INDEX_SYMBOLS,
)

logger = logging.getLogger(__name__)


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
    ticker_data = get_ticker_data(INDEX_SYMBOLS)
    message = build_market_update_message(ticker_data, prefix="")
    logger.info("Message to post:\n%s", message)

    if DEBUG:
        logging.info("Debug mode is enabled. No post will be made.")
        return True
    response = client.post(message)
    if response:
        logging.info("Post successful. Response: %s", response)
        return True
    else:
        logging.error("Failed to post update.")
        return False


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
