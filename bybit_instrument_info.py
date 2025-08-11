import os
from dotenv import load_dotenv
from pybit.unified_trading import HTTP

load_dotenv()

client = HTTP(
    api_key=os.getenv("BYBIT_API_KEY"),
    api_secret=os.getenv("BYBIT_API_SECRET"),
    testnet=False  # поставь True если используешь тестовую сеть
)


def _count_decimals(value: str) -> int:
    """Return number of decimal places in a numeric string."""
    if "." in value:
        return len(value.split(".")[1].rstrip("0"))
    return 0


def get_instrument_info(symbol: str = "BTCUSDT", category: str = "spot"):
    data = client.get_instruments_info(category=category, symbol=symbol)
    item = data["result"]["list"][0]

    lot_size = item["lotSizeFilter"]
    price_filter = item["priceFilter"]

    min_qty_str = str(lot_size["minOrderQty"])
    tick_size_str = str(price_filter["tickSize"])

    return {
        "min_qty": float(min_qty_str),
        "qty_precision": _count_decimals(min_qty_str),
        "price_precision": _count_decimals(tick_size_str),
        "tick_size": float(tick_size_str),
    }
