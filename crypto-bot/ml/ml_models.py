
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier

def get_models():
    return {
        "RandomForest": RandomForestClassifier(),
        "LightGBM": LGBMClassifier(),
        "XGBoost": XGBClassifier(),
        "CatBoost": CatBoostClassifier(verbose=0)
    }
