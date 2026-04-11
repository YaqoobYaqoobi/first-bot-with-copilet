import mysql.connector

def setup_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""   # اگر رمز داری اینجا تغییر بده
    )
    cursor = conn.cursor()

    # ساخت دیتابیس
    cursor.execute("CREATE DATABASE IF NOT EXISTS crypto_bot")
    cursor.execute("USE crypto_bot")

    # جدول معاملات اصلی
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INT AUTO_INCREMENT PRIMARY KEY,
        symbol VARCHAR(20),
        action VARCHAR(10),
        amount DECIMAL(18,8),
        price DECIMAL(18,8),
        entry_price DECIMAL(18,8),
        exit_price DECIMAL(18,8),
        stop_loss DECIMAL(18,8),
        take_profit DECIMAL(18,8),
        trailing_stop DECIMAL(18,8),
        profit_loss DECIMAL(18,8),
        strategy VARCHAR(50),
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # جدول سیگنال‌ها
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS signals (
        id INT AUTO_INCREMENT PRIMARY KEY,
        symbol VARCHAR(20),
        decision VARCHAR(10),
        confidence FLOAT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # جدول معاملات دمو
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trades_demo (
        id INT AUTO_INCREMENT PRIMARY KEY,
        symbol VARCHAR(20),
        entry_price DECIMAL(18,8),
        exit_price DECIMAL(18,8),
        stop_loss DECIMAL(18,8),
        take_profit DECIMAL(18,8),
        trailing_stop DECIMAL(18,8),
        profit_loss DECIMAL(18,8),
        timestamp_entry DATETIME,
        timestamp_exit DATETIME,
        decision_source VARCHAR(50)
    )
    """)

    # جدول عملکرد مدل‌ها
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS models_performance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        model_name VARCHAR(50),
        accuracy FLOAT,
        precision_score FLOAT,
        recall_score FLOAT,
        f1_score FLOAT,
        last_trained DATETIME
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Database setup completed!")

if __name__ == "__main__":
    setup_database()
