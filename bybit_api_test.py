from pybit.unified_trading import HTTP
import os
from dotenv import load_dotenv

load_dotenv()

client = HTTP(
    api_key=os.getenv("BYBIT_API_KEY"),
    api_secret=os.getenv("BYBIT_API_SECRET"),
    testnet=True  # тестовая сеть
)

# Получить баланс
resp = client.get_wallet_balance()
print(resp)


