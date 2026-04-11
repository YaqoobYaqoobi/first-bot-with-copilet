import pandas as pd
from trading.trading import save_demo_trade   # مسیر درست
from decision_engine import make_decision
from ai_model import process_news

def run_backtest(symbol="BTCUSDT", historical_data=None, news_data=None):
    results = []
    balance = 10000  # سرمایه اولیه فرضی
    position = None

    for i in range(len(historical_data)):
        market_data = {
            "rsi": historical_data.iloc[i]["rsi"],
            "macd": historical_data.iloc[i]["macd"],
            "ema": historical_data.iloc[i]["ema"],
            "trend_score": historical_data.iloc[i]["trend_score"]
        }

        fundamental_data = process_news(news_data) if news_data else {"sentiment_score": 0}
        decision, votes = make_decision(market_data, fundamental_data, symbol)
        price = historical_data.iloc[i]["close_price"]

        if decision == "BUY" and position is None:
            position = price
            save_demo_trade(symbol, price, None, price*0.95, price*1.05, None, None, "Backtest")
            results.append({"action": "BUY", "price": price, "votes": votes})

        elif decision == "SELL" and position is not None:
            profit = price - position
            balance += profit
            save_demo_trade(symbol, position, price, None, None, None, profit, "Backtest")
            results.append({"action": "SELL", "price": price, "profit": profit, "votes": votes})
            position = None

    return results, balance
