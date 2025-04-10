import logging
import os

from dotenv import load_dotenv

load_dotenv()

BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")
BLUESKY_PASSWORD = os.getenv("BLUESKY_PASSWORD")
DEBUG = os.getenv("DEBUG").lower() == "true"

# S&P 500, Nasdaq-100, Dow Jones, Russell 2000
INDEX_SYMBOLS = ["SPY", "QQQ", "DIA", "IWM"]

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
