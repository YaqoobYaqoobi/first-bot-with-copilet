from ml.ml_models import get_models
from ai_model import analyze_market
from deep_learning.lstm_predict import predict_with_lstm

def make_decision(market_data, fundamental_data, symbol="BTCUSDT"):
    votes = []

    # 1️⃣ تصمیم مدل‌های ML
    models = get_models()
    for name, model in models.items():
        try:
            prediction = model.predict([market_data])[0]
            votes.append(prediction)
        except Exception as e:
            print(f"Model {name} error: {e}")

    # 2️⃣ تصمیم LSTM
    lstm_decision, predicted, current = predict_with_lstm(symbol)
    votes.append(lstm_decision)

    # 3️⃣ تصمیم AI تحلیلگر
    ai_decision = analyze_market(market_data, fundamental_data)
    votes.append(ai_decision)

    # 4️⃣ سیستم رأی‌گیری
    buy_votes = votes.count("BUY")
    sell_votes = votes.count("SELL")
    hold_votes = votes.count("HOLD")

    if buy_votes > sell_votes and buy_votes > hold_votes:
        final_decision = "BUY"
    elif sell_votes > buy_votes and sell_votes > hold_votes:
        final_decision = "SELL"
    else:
        final_decision = "HOLD"

    return final_decision, votes
