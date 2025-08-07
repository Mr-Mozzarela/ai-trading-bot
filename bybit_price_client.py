from pybit.unified_trading import HTTP
import os
from dotenv import load_dotenv

load_dotenv()

client = HTTP(
    testnet=False  # ⛔ не подключаем ключи, т.к. только чтение
)

def get_live_price_and_volume(symbol: str) -> tuple[float, float]:
    try:
        resp = client.get_tickers(category="linear", symbol=symbol)
        data = resp["result"]["list"][0]
        return float(data["lastPrice"]), float(data["turnover24h"])
    except Exception as e:
        print("⚠️ Ошибка при получении цены:", e)
        return 0.0, 0.0

