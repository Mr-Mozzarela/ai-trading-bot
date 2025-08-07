import os
from dotenv import load_dotenv
from pybit.unified_trading import HTTP

load_dotenv()

client = HTTP(
    api_key=os.getenv("BYBIT_API_KEY"),
    api_secret=os.getenv("BYBIT_API_SECRET"),
    testnet=False  # поставь True если используешь тестовую сеть
)

def get_instrument_info(symbol="BTCUSDT", category="spot"):
    data = client.get_instruments_info(category=category, symbol=symbol)
    item = data["result"]["list"][0]

    lot_size = item["lotSizeFilter"]
    price_filter = item["priceFilter"]

    return {
        "min_qty": float(lot_size["minOrderQty"]),
        "qty_precision": len(str(lot_size["minOrderQty"]).split(".")[1]),
        "price_precision": len(str(price_filter["tickSize"]).split(".")[1]),
        "tick_size": float(price_filter["tickSize"])
    }
