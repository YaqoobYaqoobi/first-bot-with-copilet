# import mysql.connector

# def get_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",          # تغییر بده
#         password="12345",          # رمز خودت را بگذار
#         database="crypto_bot"
#     )
import mysql.connector
from datetime import datetime, date

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="crypto_bot"
    )

def init_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS crypto_bot")
    cursor.execute("USE crypto_bot")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INT AUTO_INCREMENT PRIMARY KEY,
            symbol VARCHAR(10),
            action VARCHAR(10),
            amount DECIMAL(18,8),
            price DECIMAL(18,8),
            timestamp DATETIME
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            symbol VARCHAR(10),
            price DECIMAL(18,8),
            timestamp DATETIME
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT,
            timestamp DATETIME
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

# ذخیره معامله
def save_trade(symbol, action, amount, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO trades (symbol, action, amount, price, timestamp) VALUES (%s, %s, %s, %s, %s)",
        (symbol, action, amount, price, datetime.now())
    )
    conn.commit()
    cursor.close()
    conn.close()

# خواندن همه معاملات
def get_trades():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM trades ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# فیلتر: معاملات یک ارز خاص
def get_trades_by_symbol(symbol):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM trades WHERE symbol=%s ORDER BY timestamp DESC", (symbol,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# فیلتر: معاملات امروز
def get_trades_today():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    today = date.today()
    cursor.execute("SELECT * FROM trades WHERE DATE(timestamp)=%s ORDER BY timestamp DESC", (today,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# ذخیره قیمت
def save_price(symbol, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO prices (symbol, price, timestamp) VALUES (%s, %s, %s)",
        (symbol, price, datetime.now())
    )
    conn.commit()
    cursor.close()
    conn.close()

# ذخیره لاگ
def save_log(message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (message, timestamp) VALUES (%s, %s)",
        (message, datetime.now())
    )
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database and tables are ready!")
