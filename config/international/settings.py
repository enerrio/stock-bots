import os

from dotenv import load_dotenv

load_dotenv(".env.international")

BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")
BLUESKY_PASSWORD = os.getenv("BLUESKY_PASSWORD")
DEBUG = os.getenv("DEBUG").lower() == "true"

# Canada, USA, UK, Germany, France, Japan, Hong Kong, Australia
INDEX_SYMBOLS = [
    "^GSPTSE",
    "^DJI",
    "^FTSE",
    "^GDAXI",
    "^FCHI",
    "^N225",
    "^HSI",
    "^AXJO",
]
