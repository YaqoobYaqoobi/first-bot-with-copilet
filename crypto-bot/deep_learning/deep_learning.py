import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from database.db import get_connection # type: ignore






def prepare_data(symbol="BTCUSDT", time_steps=60):
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT close_price, timestamp FROM market_data WHERE symbol=%s ORDER BY timestamp ASC", (symbol,))
    rows = cursor.fetchall()
    cursor.close()
    db.close()

    data = pd.DataFrame(rows)
    prices = data['close_price'].values.reshape(-1,1)

    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_prices = scaler.fit_transform(prices)

    X, y = [], []
    for i in range(time_steps, len(scaled_prices)):
        X.append(scaled_prices[i-time_steps:i, 0])
        y.append(scaled_prices[i, 0])
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    return X, y, scaler

def build_lstm(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_lstm(symbol="BTCUSDT"):
    X, y, scaler = prepare_data(symbol)
    model = build_lstm((X.shape[1],1))
    model.fit(X, y, epochs=20, batch_size=32)
    model.save(f"models/lstm_{symbol}.h5")
    print(f"LSTM model for {symbol} trained and saved.")

def predict_lstm(symbol="BTCUSDT"):
    try:
        model = load_model(f"models/lstm_{symbol}.h5")
        X, _, scaler = prepare_data(symbol)
        prediction = model.predict(X[-1].reshape(1, X.shape[1], 1))
        predicted_price = scaler.inverse_transform(prediction)[0][0]
        return predicted_price
    except Exception as e:
        print("Prediction error:", e)
        return None
