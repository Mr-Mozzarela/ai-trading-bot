from pybit.unified_trading import HTTP
import os
from dotenv import load_dotenv

load_dotenv()

client = HTTP(
    api_key=os.getenv("BYBIT_API_KEY"),
    api_secret=os.getenv("BYBIT_API_SECRET")
)

def get_price_volume(symbol: str):
    response = client.get_tickers(category="linear", symbol=symbol)
    ticker = response["result"]["list"][0]
    price = float(ticker["lastPrice"])
    volume = float(ticker["turnover24h"])
    return price, volume

