import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.db import get_connection

def save_demo_trade(symbol, entry_price, exit_price, stop_loss, take_profit, trailing_stop, profit_loss, decision_source):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO trades_demo (symbol, entry_price, exit_price, stop_loss, take_profit, trailing_stop, profit_loss, timestamp_entry, timestamp_exit, decision_source)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), %s)
    """, (symbol, entry_price, exit_price, stop_loss, take_profit, trailing_stop, profit_loss, decision_source))
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Demo trade saved!")
