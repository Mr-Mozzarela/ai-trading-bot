from pybit.unified_trading import HTTP
import os
from dotenv import load_dotenv

load_dotenv()

client = HTTP(
    api_key=os.getenv("BYBIT_API_KEY"),
    api_secret=os.getenv("BYBIT_API_SECRET"),
    testnet=os.getenv("BYBIT_TESTNET", "true").lower() == "true"
)

def get_price(symbol: str) -> float:
    resp = client.get_tickers(category="linear", symbol=symbol)
    return float(resp["result"]["list"][0]["lastPrice"])

def place_order(symbol: str, side: str, qty: float, price: float) -> dict:
    return client.place_order(
        category="linear",
        symbol=symbol,
        side=side,  # "Buy" или "Sell"
        orderType="Limit",
        qty=qty,
        price=price,
        timeInForce="GTC"
    )

def cancel_all_orders(symbol: str) -> dict:
    return client.cancel_all_orders(
        category="linear",
        symbol=symbol
    )

