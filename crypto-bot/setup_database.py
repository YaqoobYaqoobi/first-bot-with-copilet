import mysql.connector

def setup_database():
    # اتصال اولیه بدون دیتابیس
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""   # رمز خودت اگر داری
    )

    cursor = conn.cursor()

    # ساخت دیتابیس
    cursor.execute("CREATE DATABASE IF NOT EXISTS crypto_bot")

    # انتخاب دیتابیس
    cursor.execute("USE crypto_bot")

    # ساخت جدول trades
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INT AUTO_INCREMENT PRIMARY KEY,
        symbol VARCHAR(20),
        entry_price FLOAT,
        exit_price FLOAT,
        stop_loss FLOAT,
        take_profit FLOAT,
        trailing_stop FLOAT,
        result VARCHAR(20),
        strategy VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ساخت جدول signals
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS signals (
        id INT AUTO_INCREMENT PRIMARY KEY,
        symbol VARCHAR(20),
        decision VARCHAR(10),
        confidence FLOAT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("Database setup completed!")

if __name__ == "__main__":
    setup_database()