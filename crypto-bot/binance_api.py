import os
from binance.client import Client
from dotenv import load_dotenv

# بارگذاری کلیدها از .env
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# اتصال به Binance
client = Client(API_KEY, API_SECRET)

def get_price(symbol="BTCUSDT"):
    """دریافت قیمت لحظه‌ای"""
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

def place_order(symbol, side, quantity, price=None, order_type="MARKET"):
    """ارسال سفارش خرید/فروش"""
    if order_type == "MARKET":
        order = client.create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )
    else:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=str(price)
        )
    return order
