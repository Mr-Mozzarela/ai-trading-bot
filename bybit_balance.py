from pybit.unified_trading import HTTP
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_API_SECRET")

client = HTTP(
    api_key=API_KEY,
    api_secret=API_SECRET
)

def get_usdt_balance():
    balances = client.get_wallet_balance(accountType="UNIFIED")["result"]["list"][0]["coin"]
    return float(next(coin["walletBalance"] for coin in balances if coin["coin"] == "USDT"))

def get_token_balance(symbol: str):
    balances = client.get_wallet_balance(accountType="UNIFIED")["result"]["list"][0]["coin"]
    for coin in balances:
        if coin["coin"] == symbol.upper():
            return float(coin["walletBalance"])
    return 0.0

