from db import get_connection

def save_demo_trade(symbol, entry, exit, sl, tp, ts, pl, source):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO trades_demo (symbol, entry_price, exit_price, stop_loss, take_profit, trailing_stop, profit_loss, timestamp_entry, timestamp_exit, decision_source)
        VALUES (%s,%s,%s,%s,%s,%s,%s,NOW(),NOW(),%s)
    """, (symbol, entry, exit, sl, tp, ts, pl, source))
    db.commit()
    cursor.close()
    db.close()

def apply_risk_management(entry_price, decision):
    stop_loss = entry_price * 0.98   # 2% پایین‌تر
    take_profit = entry_price * 1.05 # 5% بالاتر
    trailing_stop = 0.02             # 2% trailing
    return stop_loss, take_profit, trailing_stop
