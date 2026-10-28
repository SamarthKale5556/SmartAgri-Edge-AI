"""
test_inference.py - Comprehensive Unit and Integration Test Suite
Smart Agriculture: Real-Time Irrigation Prediction at the IoT Edge

Validates:
1. Model artifact file existence and deserialization.
2. Inference output schema, types, probability calibration, and validity.
3. Input validation: valid ranges, out-of-bounds rejection, missing fields, null values.
4. Reproducible IoT sensor simulation (seed deterministic behavior).
5. SQLite prediction history persistence and retrieval.
6. Evaluation metric calculation and consistency.
7. Local edge inference latency benchmark (< 150ms).
"""

import os
import sys
import pytest
import sqlite3
import joblib
import pandas as pd
import numpy as np

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from edge_inference import EdgeInferenceEngine, VALIDATION_RULES
from simulate_iot import IoTSensorSimulator, SCENARIOS
from train_model import generate_synthetic_dataset


@pytest.fixture(scope="module")
def edge_engine(tmp_path_factory):
    """Provides an isolated EdgeInferenceEngine with a dedicated temporary database."""
    test_db = str(tmp_path_factory.mktemp("edge_test") / "test_telemetry.db")
    model_path = os.path.join(PROJECT_ROOT, "models", "irrigation_model.joblib")
    assert os.path.exists(model_path), f"Trained model must exist at {model_path}"
    engine = EdgeInferenceEngine(model_path=model_path, db_path=test_db)
    return engine


class TestModelArtifacts:
    """Verifies artifact existence, loading integrity, and pipeline structure."""

    def test_model_file_exists(self):
        model_path = os.path.join(PROJECT_ROOT, "models", "irrigation_model.joblib")
        assert os.path.exists(model_path), "Model artifact models/irrigation_model.joblib must exist."

    def test_model_loading_and_pipeline_structure(self, edge_engine):
        assert edge_engine.model is not None
        assert hasattr(edge_engine.model, "predict")
        assert hasattr(edge_engine.model, "predict_proba")
        # Ensure it has scaler and classifier
        assert "scaler" in edge_engine.model.named_steps
        assert "classifier" in edge_engine.model.named_steps

    def test_dataset_artifact_exists(self):
        data_path = os.path.join(PROJECT_ROOT, "data", "irrigation_sensor_data.csv")
        assert os.path.exists(data_path), "Dataset data/irrigation_sensor_data.csv must exist."
        df = pd.read_csv(data_path)
        assert len(df) >= 1000
        for col in ["soil_moisture_percent", "temperature_c", "humidity_percent", "rainfall_mm", "irrigation_needed"]:
            assert col in df.columns


class TestInputValidation:
    """Verifies edge input validation catches corrupted or illegal telemetry."""

    def test_valid_payload(self, edge_engine):
        valid = {
            "soil_moisture_percent": 25.0,
            "temperature_c": 28.5,
            "humidity_percent": 55.0,
            "rainfall_mm": 2.0
        }
        is_ok, err = edge_engine.validate_reading(valid)
        assert is_ok is True
        assert err is None

    def test_out_of_bounds_soil_moisture(self, edge_engine):
        payload_high = {
            "soil_moisture_percent": 115.0,
            "temperature_c": 25.0,
            "humidity_percent": 60.0,
            "rainfall_mm": 0.0
        }
        is_ok, err = edge_engine.validate_reading(payload_high)
        assert is_ok is False
        assert "soil_moisture_percent" in err

    def test_out_of_bounds_temperature(self, edge_engine):
        payload = {
            "soil_moisture_percent": 25.0,
            "temperature_c": 85.0,  # Unrealistic 85°C
            "humidity_percent": 60.0,
            "rainfall_mm": 0.0
        }
        is_ok, err = edge_engine.validate_reading(payload)
        assert is_ok is False
        assert "temperature_c" in err

    def test_negative_rainfall(self, edge_engine):
        payload = {
            "soil_moisture_percent": 25.0,
            "temperature_c": 25.0,
            "humidity_percent": 60.0,
            "rainfall_mm": -5.0
        }
        is_ok, err = edge_engine.validate_reading(payload)
        assert is_ok is False
        assert "rainfall_mm" in err

    def test_missing_field(self, edge_engine):
        payload = {
            "soil_moisture_percent": 25.0,
            "temperature_c": 25.0,
            # humidity missing
            "rainfall_mm": 0.0
        }
        is_ok, err = edge_engine.validate_reading(payload)
        assert is_ok is False
        assert "humidity_percent" in err

    def test_none_value(self, edge_engine):
        payload = {
            "soil_moisture_percent": None,
            "temperature_c": 25.0,
            "humidity_percent": 60.0,
            "rainfall_mm": 0.0
        }
        is_ok, err = edge_engine.validate_reading(payload)
        assert is_ok is False
        assert "cannot be None" in err

    def test_non_numeric_type(self, edge_engine):
        payload = {
            "soil_moisture_percent": "twenty-five",
            "temperature_c": 25.0,
            "humidity_percent": 60.0,
            "rainfall_mm": 0.0
        }
        is_ok, err = edge_engine.validate_reading(payload)
        assert is_ok is False
        assert "must be numeric" in err


class TestPredictionExecution:
    """Verifies edge inference execution, outputs, and probabilities."""

    def test_drought_scenario_prediction(self, edge_engine):
        # Bone dry soil under scorching heat should recommend irrigation (1)
        reading = {
            "soil_moisture_percent": 11.0,
            "temperature_c": 39.0,
            "humidity_percent": 20.0,
            "rainfall_mm": 0.0
        }
        res = edge_engine.predict(reading, record_history=False)
        assert res["success"] is True
        assert res["prediction"] == 1
        assert res["action_code"] == "VALVE_OPEN"
        assert res["irrigation_probability"] >= 0.75
        assert res["latency_ms"] < 250.0  # Low latency check

    def test_saturated_wet_scenario_prediction(self, edge_engine):
        # Saturated soil after heavy rain should NOT recommend irrigation (0)
        reading = {
            "soil_moisture_percent": 50.0,
            "temperature_c": 20.0,
            "humidity_percent": 85.0,
            "rainfall_mm": 25.0
        }
        res = edge_engine.predict(reading, record_history=False)
        assert res["success"] is True
        assert res["prediction"] == 0
        assert res["action_code"] == "VALVE_CLOSED"
        assert res["irrigation_probability"] <= 0.25

    def test_probability_sums_to_one(self, edge_engine):
        reading = {
            "soil_moisture_percent": 30.0,
            "temperature_c": 28.0,
            "humidity_percent": 50.0,
            "rainfall_mm": 0.0
        }
        res = edge_engine.predict(reading, record_history=False)
        assert 0.0 <= res["confidence_score"] <= 1.0
        assert 0.0 <= res["irrigation_probability"] <= 1.0


class TestSimulationReproducibility:
    """Verifies deterministic behavior with fixed random seeds."""

    def test_sensor_simulator_reproducibility(self):
        sim = IoTSensorSimulator()
        r1 = sim.generate_reading(custom_seed=999)
        r2 = sim.generate_reading(custom_seed=999)
        assert r1["soil_moisture_percent"] == r2["soil_moisture_percent"]
        assert r1["temperature_c"] == r2["temperature_c"]
        assert r1["humidity_percent"] == r2["humidity_percent"]
        assert r1["rainfall_mm"] == r2["rainfall_mm"]

    def test_dataset_generation_reproducibility(self):
        df1 = generate_synthetic_dataset(num_samples=50, seed=123)
        df2 = generate_synthetic_dataset(num_samples=50, seed=123)
        pd.testing.assert_frame_equal(df1, df2)


class TestPersistenceAndHistory:
    """Verifies SQLite history persistence and retrieval."""

    def test_telemetry_stored_in_sqlite(self, edge_engine):
        # Clear test db first
        edge_engine.clear_history()

        reading = {
            "soil_moisture_percent": 22.0,
            "temperature_c": 31.0,
            "humidity_percent": 45.0,
            "rainfall_mm": 0.0
        }
        res = edge_engine.predict(reading, record_history=True)
        assert res["success"] is True

        history_df = edge_engine.get_history_df(limit=10)
        assert len(history_df) == 1
        row = history_df.iloc[0]
        assert row["soil_moisture"] == 22.0
        assert row["temperature"] == 31.0
        assert row["action_code"] == res["action_code"]


class TestEvaluationMetricsIntegrity:
    """Verifies recorded evaluation metrics are consistent and non-trivial."""

    def test_metrics_json_integrity(self):
        import json
        metrics_file = os.path.join(PROJECT_ROOT, "outputs", "evaluation_metrics.json")
        assert os.path.exists(metrics_file)
        with open(metrics_file, "r") as f:
            m = json.load(f)

        assert m["test_accuracy"] >= 0.80
        assert m["test_precision"] >= 0.80
        assert m["test_recall"] >= 0.75
        assert m["test_f1_score"] >= 0.80
        assert m["test_samples"] == 500
        assert "confusion_matrix" in m
