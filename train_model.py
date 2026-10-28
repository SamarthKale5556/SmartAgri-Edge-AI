"""
train_model.py - Dataset Generation and Model Training Pipeline
Smart Agriculture: Real-Time Irrigation Prediction at the IoT Edge

This script:
1. Generates a reproducible synthetic agro-climatic sensor dataset (fixed random seed = 42).
2. Explicitly labels the data as SYNTHETIC with documented generation rules.
3. Performs a stratified train-test split (80% train / 20% test).
4. Trains a scikit-learn Pipeline (StandardScaler + RandomForestClassifier) strictly avoiding data leakage.
5. Evaluates metrics (Accuracy, Precision, Recall, F1, Confusion Matrix).
6. Serializes the trained pipeline to models/irrigation_model.joblib.
7. Saves evaluation metrics and dataset assumptions to outputs/.
"""

import os
import json
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

# Constants & Paths
RANDOM_SEED = 42
NUM_SAMPLES = 2500
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

DATA_PATH = os.path.join(DATA_DIR, "irrigation_sensor_data.csv")
MODEL_PATH = os.path.join(MODELS_DIR, "irrigation_model.joblib")
METRICS_PATH = os.path.join(OUTPUTS_DIR, "evaluation_metrics.json")
CONFUSION_MATRIX_PATH = os.path.join(OUTPUTS_DIR, "confusion_matrix.png")
ASSUMPTIONS_PATH = os.path.join(OUTPUTS_DIR, "dataset_assumptions.json")


def generate_synthetic_dataset(num_samples: int = NUM_SAMPLES, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """
    Generate synthetic sensor readings with agronomic-informed ground truth logic.
    
    IMPORTANT DISCLAIMER:
    This dataset is SYNTHETIC and generated using physical-heuristic simulation rules.
    It does NOT represent physical in-situ farm sensor deployments.
    High model scores on synthetic data reflect alignment with the generator's rule set
    rather than proven field performance on live crops.
    """
    np.random.seed(seed)

    # 1. Simulate ambient temperature (°C) - typical temperate/subtropical growing season (15°C to 42°C)
    temperature_c = np.random.uniform(15.0, 42.0, num_samples)

    # 2. Simulate relative air humidity (%) - negatively correlated with temperature with noise
    humidity_base = 90.0 - 1.2 * (temperature_c - 15.0)
    humidity_percent = np.clip(humidity_base + np.random.normal(0, 10.0, num_samples), 15.0, 95.0)

    # 3. Simulate recent rainfall (mm) - skewed distribution (most days zero/minimal, occasional rain events)
    rain_occurred = np.random.binomial(1, 0.25, num_samples)
    rainfall_mm = rain_occurred * np.random.exponential(scale=6.0, size=num_samples)
    rainfall_mm = np.round(np.clip(rainfall_mm, 0.0, 45.0), 1)

    # 4. Simulate volumetric soil moisture (%) - influenced by rainfall and ambient evaporation
    moisture_base = np.random.uniform(10.0, 50.0, num_samples)
    soil_moisture_percent = moisture_base + 0.6 * rainfall_mm - 0.25 * (temperature_c - 25.0)
    soil_moisture_percent = np.round(np.clip(soil_moisture_percent, 8.0, 60.0), 1)
    temperature_c = np.round(temperature_c, 1)
    humidity_percent = np.round(humidity_percent, 1)

    # 5. Agronomic ground truth rule generation
    # Atmospheric Evaporative Demand Index (ED)
    evap_demand = (temperature_c / 35.0) * (1.0 - (humidity_percent / 100.0))
    # Soil Moisture Deficit relative to standard field capacity (38%)
    moisture_deficit = np.maximum(0.0, (36.0 - soil_moisture_percent) / 36.0)
    # Rain suppression factor
    rain_suppression = np.clip(rainfall_mm / 8.0, 0.0, 1.0)

    # Combined irrigation index with realistic stochastic variance
    propensity = (0.55 * moisture_deficit) + (0.35 * evap_demand) - (0.50 * rain_suppression)
    noise = np.random.normal(0.0, 0.06, num_samples)
    final_score = propensity + noise

    # Strict physical boundary overrides
    irrigation_needed = (final_score > 0.18).astype(int)

    # Hard overrides reflecting agronomic realities:
    # Extremely dry soil (<18%) with no heavy rain always needs irrigation
    irrigation_needed[(soil_moisture_percent < 18.0) & (rainfall_mm < 3.0)] = 1
    # Wet soil (>45%) or recent heavy rain (>15mm) never needs irrigation
    irrigation_needed[(soil_moisture_percent > 44.0) | (rainfall_mm > 14.0)] = 0

    # Introduce 3.5% random stochastic label flip (simulating micro-climate anomalies, sensor drift)
    flip_mask = np.random.binomial(1, 0.035, num_samples).astype(bool)
    irrigation_needed[flip_mask] = 1 - irrigation_needed[flip_mask]

    df = pd.DataFrame({
        "soil_moisture_percent": soil_moisture_percent,
        "temperature_c": temperature_c,
        "humidity_percent": humidity_percent,
        "rainfall_mm": rainfall_mm,
        "irrigation_needed": irrigation_needed,
    })

    return df


def save_assumptions_metadata():
    """Document data generation assumptions and model metadata."""
    metadata = {
        "dataset_type": "Synthetic (Agronomic Heuristic Simulation)",
        "random_seed": RANDOM_SEED,
        "num_samples": NUM_SAMPLES,
        "features": [
            {
                "name": "soil_moisture_percent",
                "unit": "% (volumetric)",
                "range": "8.0 - 60.0",
                "description": "Volumetric soil water content measured in crop root zone."
            },
            {
                "name": "temperature_c",
                "unit": "°C",
                "range": "15.0 - 42.0",
                "description": "Ambient canopy air temperature."
            },
            {
                "name": "humidity_percent",
                "unit": "%",
                "range": "15.0 - 95.0",
                "description": "Relative air humidity influencing evapotranspiration."
            },
            {
                "name": "rainfall_mm",
                "unit": "mm",
                "range": "0.0 - 45.0",
                "description": "Precipitation recorded over the preceding 24-hour observation window."
            }
        ],
        "target": {
            "name": "irrigation_needed",
            "classes": {
                "0": "No irrigation needed (Soil moisture adequate or recent rain)",
                "1": "Irrigation recommended (Soil water deficit under atmospheric demand)"
            }
        },
        "generation_logic": {
            "evaporative_demand_factor": "Scaled product of temperature and dryness index",
            "soil_deficit_factor": "Moisture deficit relative to 36% field capacity",
            "rain_suppression_factor": "Precipitation threshold suppression up to 8mm",
            "stochastic_noise": "Gaussian perturbation std=0.06 plus 3.5% sensor/microclimate label flips",
            "hard_boundary_rules": [
                "soil_moisture < 18% and rainfall < 3mm forces irrigation=1",
                "soil_moisture > 44% or rainfall > 14mm forces irrigation=0"
            ]
        },
        "critical_honesty_notice": (
            "Good validation scores on synthetic rule-generated data reflect consistency "
            "with the mathematical generation assumptions. It does not establish real-world "
            "agricultural accuracy on physical crops or live farm microclimates."
        )
    }

    with open(ASSUMPTIONS_PATH, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"[ASSUMPTIONS] Saved dataset metadata to {ASSUMPTIONS_PATH}")


def train_and_evaluate():
    """Execute complete reproducible training and evaluation pipeline."""
    print("=================================================================")
    print("Smart Agriculture: Edge Irrigation Classifier Training Pipeline")
    print("=================================================================")

    # 1. Dataset Generation
    df = generate_synthetic_dataset(num_samples=NUM_SAMPLES, seed=RANDOM_SEED)
    df.to_csv(DATA_PATH, index=False)
    print(f"[DATA] Generated {len(df)} synthetic records -> {DATA_PATH}")
    print(f"[DATA] Class distribution:\n{df['irrigation_needed'].value_counts(normalize=True).round(3)}")

    save_assumptions_metadata()

    # 2. Features and Target
    feature_cols = ["soil_moisture_percent", "temperature_c", "humidity_percent", "rainfall_mm"]
    X = df[feature_cols]
    y = df["irrigation_needed"]

    # 3. Stratified Train-Test Split (80% train / 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=RANDOM_SEED, stratify=y
    )
    print(f"[SPLIT] Training samples: {len(X_train)} | Test samples: {len(X_test)}")

    # 4. Pipeline with StandardScaler + RandomForest (Strictly preventing data leakage)
    # Scaler is fitted ONLY on training data inside the pipeline
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", RandomForestClassifier(
            n_estimators=100,
            max_depth=6,
            min_samples_split=4,
            min_samples_leaf=2,
            random_state=RANDOM_SEED,
            n_jobs=-1
        ))
    ])

    print("[TRAIN] Fitting scikit-learn Pipeline (StandardScaler + RandomForestClassifier)...")
    pipeline.fit(X_train, y_train)

    # 5. Held-Out Test Evaluation
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred))
    rec = float(recall_score(y_test, y_pred))
    f1 = float(f1_score(y_test, y_pred))
    cm = confusion_matrix(y_test, y_pred).tolist()

    # Feature Importances from Random Forest
    rf_model = pipeline.named_steps["classifier"]
    importances = dict(zip(feature_cols, [float(v) for v in rf_model.feature_importances_]))

    metrics = {
        "model_name": "RandomForest_Irrigation_Classifier",
        "model_version": "1.0.0",
        "framework": "scikit-learn",
        "pipeline_stages": ["StandardScaler", "RandomForestClassifier"],
        "dataset_size_total": int(len(df)),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "features": feature_cols,
        "test_accuracy": round(acc, 4),
        "test_precision": round(prec, 4),
        "test_recall": round(rec, 4),
        "test_f1_score": round(f1, 4),
        "confusion_matrix": {
            "tn": cm[0][0],
            "fp": cm[0][1],
            "fn": cm[1][0],
            "tp": cm[1][1],
            "matrix": cm
        },
        "feature_importances": importances,
        "evaluation_notes": (
            "Evaluated strictly on held-out test split (20%). "
            "Metrics reflect strong discriminative capacity on the synthetic agro-heuristic domain."
        )
    }

    print(f"\n--- HELD-OUT TEST EVALUATION RESULTS ---")
    print(f"Accuracy : {acc * 100:.2f}%")
    print(f"Precision: {prec * 100:.2f}%")
    print(f"Recall   : {rec * 100:.2f}%")
    print(f"F1-Score : {f1 * 100:.2f}%")
    print(f"Confusion Matrix (TN, FP / FN, TP):\n{np.array(cm)}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # 6. Save Model Artifact
    joblib.dump(pipeline, MODEL_PATH)
    print(f"[SAVE] Serialized model pipeline -> {MODEL_PATH}")

    # 7. Save Metrics JSON
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=4)
    print(f"[SAVE] Evaluation metrics saved -> {METRICS_PATH}")

    # 8. Generate and Save Confusion Matrix Plot
    plt.figure(figsize=(5.5, 4.5), dpi=150)
    cm_arr = np.array(cm)
    plt.imshow(cm_arr, interpolation="nearest", cmap=plt.cm.Blues)
    plt.title("Held-Out Test Confusion Matrix\n(Edge Irrigation Classifier)", fontsize=11, fontweight="bold")
    plt.colorbar()
    tick_marks = np.arange(2)
    plt.xticks(tick_marks, ["No (0)", "Yes (1)"])
    plt.yticks(tick_marks, ["No (0)", "Yes (1)"])

    thresh = cm_arr.max() / 2.0
    for i in range(cm_arr.shape[0]):
        for j in range(cm_arr.shape[1]):
            plt.text(
                j, i, format(cm_arr[i, j], "d"),
                ha="center", va="center",
                color="white" if cm_arr[i, j] > thresh else "black",
                fontweight="bold"
            )

    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")
    plt.tight_layout()
    plt.savefig(CONFUSION_MATRIX_PATH)
    plt.close()
    print(f"[SAVE] Confusion matrix plot saved -> {CONFUSION_MATRIX_PATH}")

    return metrics


if __name__ == "__main__":
    train_and_evaluate()
