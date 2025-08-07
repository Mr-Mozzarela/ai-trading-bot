from gpt_advisor import ask_gpt

price = 29500
volume = 100000000
pnl = 12.35

prompt = f"""
Анализ цены BTCUSDT: {price} USDT
Объём торгов: {volume}
Текущий PnL: {pnl} USDT

Что ты посоветуешь? Стоит ли перестроить сетку?
"""

response = ask_gpt(prompt)
print("GPT совет:", response)

