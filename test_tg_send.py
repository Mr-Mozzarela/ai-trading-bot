import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

load_dotenv()

bot = Bot(
    token=os.getenv("TELEGRAM_BOT_TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

async def send():
    user_id = int(os.getenv("TELEGRAM_USER_ID"))
    await bot.send_message(user_id, "✅ Тестовое сообщение от Telegram-бота!")
    await bot.session.close()  # ⬅️ важно: закрыть сессию после отправки

if __name__ == "__main__":
    asyncio.run(send())

