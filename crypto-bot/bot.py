from decision_engine import make_decision
from trading import save_demo_trade, apply_risk_management
from telegram_bot import send_message
import os
from setup_database import setup_database

setup_database()

def main():
    mode = os.getenv("MODE", "demo")

    # داده‌های نمونه (در عمل از دیتابیس یا API گرفته می‌شوند)
    market_data = {"rsi": 65, "macd": 0.4, "ema": 70000, "trend_score": 1.2}
    fundamental_data = {"sentiment_score": 0.5}

    decision, votes = make_decision(market_data, fundamental_data, "BTCUSDT")
    entry_price = 70000
    sl, tp, ts = apply_risk_management(entry_price, decision)

    if decision == "BUY":
        if mode == "demo":
            save_demo_trade("BTCUSDT", entry_price, None, sl, tp, ts, None, "VotingSystem")
            send_message(f"[DEMO] Final Decision: BUY | SL={sl} | TP={tp} | Votes={votes}")
        else:
            send_message(f"[REAL] Final Decision: BUY | SL={sl} | TP={tp} | Votes={votes}")

    elif decision == "SELL":
        send_message(f"Final Decision: SELL | Votes={votes}")
    else:
        send_message(f"Final Decision: HOLD | Votes={votes}")

if __name__ == "__main__":
    main()
