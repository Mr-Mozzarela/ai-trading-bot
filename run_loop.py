import asyncio
import time
from simulate_session import run as run_simulation

async def loop():
    print("🔁 Бот запущен в цикле (интервал: 15 минут)...\n")
    while True:
        try:
            print("🕒 Запуск новой сессии...")
            await run_simulation()
            print("✅ Сессия завершена\n")
        except Exception as e:
            print("⚠️ Ошибка в сессии:", e)
        await asyncio.sleep(15 * 60)  # 15 минут

if __name__ == "__main__":
    asyncio.run(loop())

