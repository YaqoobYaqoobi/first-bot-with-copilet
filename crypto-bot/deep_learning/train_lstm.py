import sys
import os

# مسیر پوشه‌ی اصلی پروژه (crypto-bot) را اضافه می‌کنیم
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# اتصال به دیتابیس
from database.db import get_connection

def train_lstm():
    # داده نمونه (اینجا داده واقعی‌ات را جایگزین کن)
    data = np.array([1,2,3,4,5,6,7,8,9,10]).reshape(-1,1)
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    X, y = [], []
    for i in range(len(data_scaled)-3):
        X.append(data_scaled[i:i+3])
        y.append(data_scaled[i+3])
    X, y = np.array(X), np.array(y)

    # ساخت مدل LSTM
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(X.shape[1], X.shape[2])))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    # آموزش مدل
    model.fit(X, y, epochs=50, verbose=0)

    # ذخیره نتایج در دیتابیس
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO models_performance (model_name, accuracy, precision_score, recall_score, f1_score, last_trained)
        VALUES (%s, %s, %s, %s, %s, NOW())
    """, ("LSTM", 1.0, 0.0, 0.0, 0.0))  # اینجا مقادیر نمونه گذاشتم
    conn.commit()
    cursor.close()
    conn.close()

    print("✅ LSTM training completed and results saved!")

if __name__ == "__main__":
    train_lstm()
