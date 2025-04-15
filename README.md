# Stock Bots
Three Bluesky bots that post regular updates on major financial indices around the world. All bots are deployed through AWS Lambda and AWS EventBridge for scheduled execution.

## Bots Overview

- **Domestic Bot:** Posts updates on major U.S. indices (SPY, QQQ, DIA, IWM) every half hour during market hours.
- **International Bot:** Posts updates for international indices (Canada, USA, UK, Germany, France, Japan, Hong Kong, Australia) every half hour on weekdays.
- **Futures Bot:** Posts updates on futures such as S&P 500 E-mini and others. The bot checks market hours before posting.


## Domestic Bot
This bot can be found at [@tickrbot.bsky.social](https://bsky.app/profile/tickrbot.bsky.social). It posts every half hour during market hours the latest prices for the following major indexes:

* SPY – S&P 500
* QQQ – Nasdaq-100
* DIA – Dow Jones
* IWM – Russell 2000

## International Bot
The international stock bot is [@tickrbotintl.bsky.social](https://bsky.app/profile/tickrbotintl.bsky.social) and posts every half hour Monday through Friday for several international markets. There are periods of the day where a market is closed but the bot posts the latest updates anyway to keep the post content consistent from post to post. The following tickers are tracked:

* ^GSPTSE - S&P/TSX Composite index (Canada)
* ^DJI - Dow Jones (USA)
* ^FTSE – FTSE 100 (UK)
* ^GDAXI – DAX (Germany)
* ^FCHI – CAC 40 (France)
* ^N225 – Nikkei 225 (Japan)
* ^HSI – Hang Seng (Hong Kong)
* ^AXJO – ASX 200 (Australia)

## Futures Bot
The [@tickrbotfutures.bsky.social](https://bsky.app/profile/tickrbotfutures.bsky.social) bot posts updates on the futures market. The following commodities are tracked:

* ES=F – S&P 500 E-mini
* NQ=F – Nasdaq 100 E-mini
* YM=F – Dow Jones Futures
* CL=F – Crude Oil
* NG=F - Natural Gas
* GC=F – Gold
* SI=F – Silver
* HG=F - Copper

## Development
This project uses [uv](https://docs.astral.sh/uv/) for Python package management and the [yfinance](https://yfinance-python.org/index.html) package for gathering ticker prices from Yahoo Finance. The [Bluesky API](https://docs.bsky.app) is used to manage posting to Bluesky.

Below is a template for what the content in the post looks like:
```
🕰️ Market Update – 1:00 PM ET

🟢 SPY - $X (+/-X%)
🔴 QQQ - $X (+/-X%)
🟢 DIA - $X (+/-X%)
🟢 <ticker> - $X (+/-X%)
```

Where 🟢 means the current price is higher than the previous trading day's close and 🔴 means it is lower. The bot is scheduled to run at the top of every hour but might be delayed by a few minutes occasionally due to AWS. All times are posted in Eastern Time Zone.

Here are some of the most relevant keys from the yfinance API that are used in this project:
* previousClose: Price at the previous trading day's close
* open: Price at market open
* regularMarketPrice: Current price
* regularMarketChangePercent: Percent change for the day
* regularMarketChange: Point change for the day

## Project Structure
Below is a description of the folders and files in this repo.
* Makefile: Contains targets to easily lint code, format code, run unit tests, and build zip files for deployment. Run with `make lint`, `make format`, `make test`, and `make package`
* bot/
  * common/
    * client.py: Bluesky client creation
    * fetch_data.py: Handles yfinance API calls to retrieve financial data
  * domestic/: Create posts on Bluesky for the domestic stock bot
  * international/: Create posts on Bluesky for the international stock bot
  * futures/: Create posts on Bluesky for the futures stock bot
* config/: Settings for each bot's BlueSky login and ticker symbols
* scripts/
  * run_bot.py: Run the bot from local machine (as opposed to automated execution via AWS Lambda)
  * package.sh: Build the zip files for each bot. These can be uploaded to each bot's Lambda function
* tests/: Unit tests

## Secrets
Not included in this repo are `.env` files that contains the login credentials for each bot's Bluesky accounts and a flag for debugging. Since we're already using AWS we could store these credentials in something more secure like [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/) but that's overkill for a small project like this.

## Deployment
This bot is deployed to AWS Lambda and is triggered by an EventBridge rule scheduled to execute every hour during market hours (excluding holidays). Here are (roughly) the commands that are run in order to prepare the code for deployment. Since there are three separate bots, the commands are a little different for each one. See the `package.sh` file for a more complete example of how to package the files together.

Install dependencies into a folder called `packages`:
```bash
uv export --frozen --no-dev --no-editable -o requirements.txt
uv pip install \
   --no-installer-metadata \
   --no-compile-bytecode \
   --python-platform x86_64-manylinux2014 \
   --python 3.13 \
   --target packages \
   -r requirements.txt
```

Then we can package the dependencies into a zip file
```bash
cd packages
zip -r ../package.zip .
cd ..

zip -r package.zip bot/domestic config/domestic .env.domestic
```

The above steps are automated in the `scripts/package.sh` shell script. The `Makefile` also includes a target to easily run that script. Simply running `make package` will execute the script and generate the zip file.

Finally, we can deploy to AWS either in the console or with the AWS CLI. I prefer to use the AWS CLI and tried experimenting with the [SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) tool but found it too cumbersome. Some other minor changes to get everything working was setting up the Eventbridge rule, IAM permissions, increasing Lambda function's timeout and memory limit up a bit from default settings, and also moving credentials out of an .env file and directly in the Lambda function's environment variables tab.
