import asyncio
from datetime import datetime
from db.models import Bot, BotSession, Order, GPTAdvice
from db.engine import async_session
from gpt_advisor import ask_gpt
from telegram_utils import TelegramBot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import os
from dotenv import load_dotenv
from bybit_market_data import get_price_volume
from bybit_instrument_info import get_instrument_info

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")

tg = TelegramBot(
    token=TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


def generate_prompt(symbol, price, volume, pnl, min_qty, tick_size):
    return f"""
Ты - советник AI грид-бота. Проанализируй рынок и предложи сетку.

Пара: {symbol}
Цена: {price} USDT
Объём: {volume}
PnL сессии: {pnl} USDT

Условия:
- Минимальный объём ордера: {min_qty}
- Шаг цены (tick size): {tick_size}

Ответ в JSON:
{{
  "action": "rebuild | hold",
  "grid_min": float,
  "grid_max": float,
  "grid_step": float,
  "cost_estimate": float,
  "reason": "коротко"
}}
"""


async def run_session():
    print("🚀 simulate_session.py запущен — вызываем run_session()...")

    symbol = "BTCUSDT"
    bot_name = "SimGridBot"
    mode = "SIMULATED"

    price, volume = get_price_volume(symbol)
    print("🚀 Сессия запущена")
    print("💰 Цена:", price, "📊 Объём:", volume)

    min_qty, qty_precision, price_precision, tick_size = get_instrument_info(symbol)

    async with async_session() as session:
        new_bot = Bot(
            name=bot_name,
            mode=mode,
            symbol=symbol,
            created_at=datetime.utcnow()
        )
        session.add(new_bot)
        await session.commit()
        await session.refresh(new_bot)

        bot_session = BotSession(
            bot_id=new_bot.id,
            start_time=datetime.utcnow(),
            pnl=14.32,
            grid=[29000, 29100, 29200, 29300, 29400]
        )
        session.add(bot_session)
        await session.commit()
        await session.refresh(bot_session)

        prompt = generate_prompt(
            symbol=symbol,
            price=price,
            volume=volume,
            pnl=bot_session.pnl,
            min_qty=min_qty,
            tick_size=tick_size
        )

        print("📤 Отправили запрос в GPT...")
        print("GPT PROMPT:", prompt)

        gpt_response = ask_gpt(prompt)

        print("✅ GPT вернул ответ длиной:", len(gpt_response))
        print("\n🧠 GPT ответ:\n", gpt_response)

        advice = GPTAdvice(
            session_id=bot_session.id,
            prompt=prompt,
            response=gpt_response,
            timestamp=datetime.utcnow()
        )
        session.add(advice)
        await session.commit()

        print("📤 Отправляем сообщение в Telegram...")
        await tg.send_message(
            TELEGRAM_USER_ID,
            f"📊 <b>{symbol}</b>\n💬 <pre>{gpt_response}</pre>"
        )


if __name__ == "__main__":
    asyncio.run(run_session())
