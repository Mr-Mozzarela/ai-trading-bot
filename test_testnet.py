from bybit_testnet_client import get_price, place_order, cancel_all_orders

symbol = "BTCUSDT"

price = get_price(symbol)
print("💰 Текущая цена:", price)

response = place_order(symbol, "Buy", qty=0.001, price=round(price * 0.99, 2))
print("📥 Ордер создан:", response)

cancel = cancel_all_orders(symbol)
print("🗑 Все ордера отменены:", cancel)

