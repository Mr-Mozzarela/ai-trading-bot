import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from dotenv import load_dotenv

from bybit_balance import get_usdt_balance, get_token_balance
from bybit_market_data import get_price_volume

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = int(os.getenv("TELEGRAM_USER_ID"))
SYMBOL = "BTCUSDT"

bot = Bot(token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("✅ Бот запущен.")

# /stop
@dp.message(Command("stop"))
async def stop_handler(message: Message):
    await message.answer("🛑 Бот остановлен.")

# /balance
@dp.message(Command("balance"))
async def balance_handler(message: Message):
    usdt = get_usdt_balance()
    token = SYMBOL.replace("USDT", "")
    token_balance = get_token_balance(token)
    price, _ = get_price_volume(SYMBOL)
    approx = round(token_balance * price, 2)

    await message.answer(
        f"<b>💰 Баланс:</b>\n"
        f"USDT: <code>{usdt}</code>\n"
        f"{token}: <code>{token_balance}</code> ≈ <code>{approx} USDT</code>"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

