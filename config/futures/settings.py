import os

from dotenv import load_dotenv

load_dotenv(".env.futures")

BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")
BLUESKY_PASSWORD = os.getenv("BLUESKY_PASSWORD")
DEBUG = os.getenv("DEBUG").lower() == "true"

# S&P 500 E-mini, Nasdaq 100 E-mini, Dow Jones Futures, Crude Oil, Natural Gas, Gold, Silver, Copper
INDEX_SYMBOLS = ["ES=F", "NQ=F", "YM=F", "CL=F", "NG=F", "GC=F", "SI=F", "HG=F"]
