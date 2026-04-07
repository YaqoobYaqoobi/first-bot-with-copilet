import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from ml_models import get_models
from db import get_connection

def train_models():
    # نمونه داده (در عمل باید داده‌های واقعی بازار از دیتابیس یا API گرفته شود)
    data = pd.DataFrame({
        "rsi": [30, 70, 55, 40, 65, 80],
        "macd": [0.5, -0.3, 0.1, -0.2, 0.4, 0.6],
        "ema": [100, 105, 102, 98, 110, 115],
        "trend_score": [1, -1, 0, -1, 1, 1],
        "label": ["BUY", "SELL", "HOLD", "SELL", "BUY", "BUY"]
    })

    X = data[["rsi", "macd", "ema", "trend_score"]]
    y = data["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    models = get_models()

    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        acc = accuracy_score(y_test, predictions) * 100
        prec = precision_score(y_test, predictions, average="macro") * 100
        rec = recall_score(y_test, predictions, average="macro") * 100
        f1 = f1_score(y_test, predictions, average="macro") * 100

        print(f"{name} → Accuracy: {acc:.2f}%")

        # ذخیره نتایج در دیتابیس
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO models_performance (model_name, accuracy, precision, recall, f1_score, last_trained)
            VALUES (%s,%s,%s,%s,%s,NOW())
        """, (name, acc, prec, rec, f1))
        db.commit()
        cursor.close()
        db.close()

if __name__ == "__main__":
    train_models()
