from decision_engine import make_decision
from trading.trading import save_demo_trade, apply_risk_management
from trading.telegram_bot import send_message
import os
from database.setup_database import setup_database
from database import db


 # اضافه کردن فایل دیتابیس

setup_database()
db.init_db()  # آماده‌سازی دیتابیس

def main():
    mode = os.getenv("MODE", "demo")

    # داده‌های نمونه (در عمل از API یا دیتابیس گرفته می‌شوند)
    market_data = {"rsi": 65, "macd": 0.4, "ema": 70000, "trend_score": 1.2}
    fundamental_data = {"sentiment_score": 0.5}

    decision, votes = make_decision(market_data, fundamental_data, "BTCUSDT")
    entry_price = 70000
    sl, tp, ts = apply_risk_management(entry_price, decision)

    if decision == "BUY":
        if mode == "demo":
            save_demo_trade("BTCUSDT", entry_price, None, sl, tp, ts, None, "VotingSystem")
            db.save_trade("BTCUSDT", "BUY", 0.01, entry_price)  # ذخیره در دیتابیس
            send_message(f"[DEMO] Final Decision: BUY | SL={sl} | TP={tp} | Votes={votes}")
        else:
            db.save_trade("BTCUSDT", "BUY", 0.01, entry_price)  # ذخیره در دیتابیس
            send_message(f"[REAL] Final Decision: BUY | SL={sl} | TP={tp} | Votes={votes}")

    elif decision == "SELL":
        db.save_trade("BTCUSDT", "SELL", 0.01, entry_price)  # ذخیره در دیتابیس
        send_message(f"Final Decision: SELL | Votes={votes}")
    else:
        db.save_log("Decision: HOLD")  # ذخیره لاگ در دیتابیس
        send_message(f"Final Decision: HOLD | Votes={votes}")

if __name__ == "__main__":
    main()
