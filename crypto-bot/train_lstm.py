import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from db import get_connection

def train_lstm(symbol="BTCUSDT"):
    # اتصال به دیتابیس و گرفتن داده‌های بازار
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT close_price, timestamp FROM market_data WHERE symbol=%s ORDER BY timestamp ASC", (symbol,))
    rows = cursor.fetchall()
    cursor.close()
    db.close()

    # تبدیل داده‌ها به DataFrame
    data = pd.DataFrame(rows)
    prices = data['close_price'].values.reshape(-1,1)

    # نرمال‌سازی داده‌ها
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_prices = scaler.fit_transform(prices)

    # ساخت داده‌های سری زمانی
    X, y = [], []
    time_steps = 60
    for i in range(time_steps, len(scaled_prices)):
        X.append(scaled_prices[i-time_steps:i, 0])
        y.append(scaled_prices[i, 0])
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    # ساخت مدل LSTM
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1],1)))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # آموزش مدل
    model.fit(X, y, epochs=20, batch_size=32)

    # ذخیره مدل
    model.save(f"models/lstm_{symbol}.h5")
    print(f"LSTM model for {symbol} trained and saved.")

if __name__ == "__main__":
    train_lstm("BTCUSDT")
