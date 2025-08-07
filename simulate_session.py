import os

if not os.path.exists("start.flag"):
    print("⛔ Торговля остановлена (нет start.flag)")
    exit()


import asyncio
from db.init_db import async_session
from db.models import Bot, BotSession, Order, GPTAdvice
from telegram_utils import TelegramBot
from bybit_market_data import get_price_volume
from bybit_instrument_info import get_instrument_info
from gpt_advisor import ask_gpt
import json
from datetime import datetime
import os
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = int(os.getenv("TELEGRAM_USER_ID"))

tg = TelegramBot(
    token=TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


def generate_prompt(symbol, price, volume, pnl, min_qty, tick_size, balance_usdt):
    return f"""
Ты — AI-советник для криптовалютного грид-бота. Твоя цель — приумножить капитал трейдера, используя сеточную торговлю.n
n
Пара: {symbol}n
Цена: {price} USDTn
Объём: {volume}n
PnL сессии: {pnl} USDTn
Текущий баланс: {balance_usdt} USDTn
n
Условия торговли:n
- Минимальный объём ордера: {min_qty}n
- Шаг цены (tick size): {tick_size}n
- Комиссия уже учтенаn
n
Проанализируй текущую рыночную ситуацию, сравни с предыдущей сеткой, учти затраты на перестройку и оцени потенциальную прибыль.n
n
Ответ строго в формате JSON:n
{{n
  "action": "rebuild | hold",n
  "grid_min": float,n
  "grid_max": float,n
  "grid_step": float,n
  "cost_estimate": float,n
  "reason": "коротко"n
}}
"""

async def run_session():
    print("🚀 Сессия запущена")
    symbol = "BTCUSDT"
    bot_name = "SimGridBot"
    mode = "SIMULATED"

    price, volume = get_price_volume(symbol)
    print("💰 Цена:", price, "📊 Объём:", volume)

    info = get_instrument_info(symbol)
    min_qty = float(info["min_qty"])
    qty_precision = int(info["qty_precision"])
    price_precision = int(info["price_precision"])
    tick_size = float(info["tick_size"])

    async with async_session() as session:
        bot = Bot(name=bot_name, mode=mode, symbol=symbol, created_at=datetime.utcnow())
        session.add(bot)
        await session.commit()
        await session.refresh(bot)

        bot_session = BotSession(bot_id=bot.id, start_time=datetime.utcnow(), pnl=0.0, grid=[])
        session.add(bot_session)
        await session.commit()
        await session.refresh(bot_session)

        # Отправка уведомления о запуске бота
        await tg.send_message(TELEGRAM_USER_ID, f"🤖 Бот <b>{symbol}</b> запущен в режиме <b>{mode}</b>")

        pnl = bot_session.pnl if bot_session else 0.0
        balance_usdt = get_usdt_balance()
        prompt = generate_prompt(symbol, price, volume, pnl, min_qty, tick_size, balance_usdt)
        # Отправка GPT запроса
        print("📤 Отправили запрос в GPT...")
        print("GPT PROMPT:", prompt)
        gpt_response = ask_gpt(prompt)
        print("✅ GPT вернул ответ длиной:", len(gpt_response))

        # Сохраняем ответ GPT в базу
        gpt_entry = GPTAdvice(
            session_id=bot_session.id,
            prompt=prompt,
            response=gpt_response,
            timestamp=datetime.utcnow()
        )
        session.add(gpt_entry)
        await session.commit()

        try:
            gpt_data = json.loads(gpt_response)
        except Exception as e:
            print("Ошибка при разборе JSON от GPT:", e)
            return

        action = gpt_data.get("action")
        grid_min = gpt_data.get("grid_min")
        grid_max = gpt_data.get("grid_max")
        grid_step = gpt_data.get("grid_step")
        cost_estimate = gpt_data.get("cost_estimate")
        reason = gpt_data.get("reason")

        # Учитываем только перестройку сетки с разумной ценой
        if action == "rebuild" and grid_min and grid_max and grid_step:
            print("📐 Начинаем строить сетку...")
            print("grid_min:", grid_min, "grid_max:", grid_max, "grid_step:", grid_step)
            new_grid = []
            level = grid_min
            while level <= grid_max:
                new_grid.append(round(level, price_precision))
                level += grid_step

            bot_session.grid = new_grid
            await session.commit()
            print("✅ Сетка построена:", new_grid)

            # Формируем ордера
            buy_orders = [lvl for lvl in new_grid if lvl < price]
            sell_orders = [lvl for lvl in new_grid if lvl > price]

            buy_text = "\n".join([f"{lvl:.{price_precision}f}" for lvl in buy_orders])
            sell_text = "\n".join([f"{lvl:.{price_precision}f}" for lvl in sell_orders])

            text = f"""
📊 <b>{symbol}</b>

<b>Buy Orders:</b>
{buy_text if buy_text else "(нет ордеров)"}

<b>Sell Orders:</b>
{sell_text if sell_text else "(нет ордеров)"}

📎 {reason}
"""
            await tg.send_message(TELEGRAM_USER_ID, text)

        # Допустим: исполнился один ордер для примера
        example_order = Order(
            session_id=bot_session.id,
            price=price,
            quantity=0.01,
            side="Buy",
            filled=0.01,
            fee=0.005,
            timestamp=datetime.utcnow()
        )
        session.add(example_order)
        await session.commit()

        await tg.send_message(TELEGRAM_USER_ID, f"✅ Исполнен ордер: BUY {example_order.quantity} по цене {example_order.price}")


if __name__ == "__main__":
    print("Запускаем run_session()...")
    asyncio.run(run_session())

