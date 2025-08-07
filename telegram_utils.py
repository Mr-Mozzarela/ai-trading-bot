from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

class TelegramBot:
    def __init__(self, token, default):
        self.bot = Bot(token=token, default=default)

    async def send_message(self, user_id, message):
        try:
            await self.bot.send_message(chat_id=user_id, text=message)
        finally:
            await self.bot.session.close()

