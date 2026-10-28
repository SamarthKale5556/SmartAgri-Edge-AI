"""
evaluate_model.py - Standalone Model Evaluation & Validation Tool
Smart Agriculture: Real-Time Irrigation Prediction at the IoT Edge

Loads the saved model artifact from models/irrigation_model.joblib and evaluates
performance on the held-out test split of data/irrigation_sensor_data.csv.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "irrigation_sensor_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "irrigation_model.joblib")
METRICS_PATH = os.path.join(BASE_DIR, "outputs", "evaluation_metrics.json")


def run_evaluation(data_path: str = DATA_PATH, model_path: str = MODEL_PATH):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model artifact not found at {model_path}. Run train_model.py first.")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}. Run train_model.py first.")

    print(f"[EVALUATE] Loading model from: {model_path}")
    pipeline = joblib.load(model_path)

    print(f"[EVALUATE] Loading dataset from: {data_path}")
    df = pd.read_csv(data_path)

    features = ["soil_moisture_percent", "temperature_c", "humidity_percent", "rainfall_mm"]
    X = df[features]
    y = df["irrigation_needed"]

    # Re-create the identical stratified test partition
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print("\n" + "=" * 50)
    print("      EVALUATION REPORT (HELD-OUT TEST SET)")
    print("=" * 50)
    print(f"Total Test Samples: {len(X_test)}")
    print(f"Accuracy          : {acc * 100:.2f}%")
    print(f"Precision         : {prec * 100:.2f}%")
    print(f"Recall            : {rec * 100:.2f}%")
    print(f"F1-Score          : {f1 * 100:.2f}%")
    print("\nConfusion Matrix:")
    print(f"  TN: {cm[0][0]:3d} | FP: {cm[0][1]:3d}")
    print(f"  FN: {cm[1][0]:3d} | TP: {cm[1][1]:3d}")
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["Adequate (0)", "Irrigate (1)"]))

    return {
        "accuracy": float(acc),
        "precision": float(prec),
        "recall": float(rec),
        "f1": float(f1),
        "confusion_matrix": cm.tolist()
    }


if __name__ == "__main__":
    run_evaluation()
