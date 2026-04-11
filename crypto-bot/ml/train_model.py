import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from ml.ml_models import get_models
from database.db import get_connection

def train_models():
    # داده نمونه (اینجا می‌توانی داده واقعی‌ات را جایگزین کنی)
    X = pd.DataFrame([[0],[1],[0],[1]], columns=["feature"])
    y = [0,1,0,1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)

    models = get_models()
    conn = get_connection()
    cursor = conn.cursor()

    for name, model in models.items():
        try:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, zero_division=0)
            rec = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)

            print(f"{name} → Accuracy: {acc*100:.2f}%")

            cursor.execute("""
                INSERT INTO models_performance 
                (model_name, accuracy, precision_score, recall_score, f1_score, last_trained)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, (name, acc, prec, rec, f1))

            conn.commit()
        except Exception as e:
            print(f"{name} error: {e}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    train_models()
