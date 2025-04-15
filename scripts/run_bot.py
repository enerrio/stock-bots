import argparse
import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_and_run_market(market: str) -> None:
    if market == "domestic":
        from bot.domestic import post as market_post
    elif market == "international":
        from bot.international import post as market_post
    elif market == "futures":
        from bot.futures import post as market_post
    else:
        raise ValueError(f"Unknown market type: {market}")
    market_post.run()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    parser = argparse.ArgumentParser(description="Run the bot.")
    parser.add_argument("--market", choices=["domestic", "international", "futures"])
    args = parser.parse_args()
    load_and_run_market(args.market)
