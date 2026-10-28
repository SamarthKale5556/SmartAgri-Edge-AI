"""
test_api.py - Automated Test Suite for AgriSense FastAPI Backend
Validates REST API endpoints, Pydantic input validation traps, and integration with the edge ML model.
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from api_server import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["system"] == "AgriSense Edge AI"
    assert "Samarth Kale" in data["workspace"]
    assert data["edge_model_loaded"] is True
    assert data["edge_model_active"] is True


def test_model_info_endpoint():
    response = client.get("/api/model-info")
    assert response.status_code == 200
    data = response.json()
    assert data["model_name"] == "RandomForest_Irrigation_Classifier"
    assert "StandardScaler" in data["pipeline_stages"]
    assert "RandomForestClassifier" in data["pipeline_stages"]
    assert len(data["input_features"]) == 4


def test_metrics_endpoint():
    response = client.get("/api/metrics")
    assert response.status_code == 200
    data = response.json()
    m = data["metrics"]
    assert m["test_accuracy"] >= 0.80
    assert m["test_precision"] >= 0.80
    assert m["test_recall"] >= 0.75
    assert m["test_f1_score"] >= 0.80
    assert data["is_synthetic"] is True


def test_predict_drought_scenario():
    payload = {
        "soil_moisture_percent": 12.5,
        "temperature_c": 38.0,
        "humidity_percent": 20.0,
        "rainfall_mm": 0.0,
        "field_zone": "North-Field-A"
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert res["prediction"] == 1
    assert res["action_code"] == "VALVE_OPEN"
    assert res["irrigation_probability"] >= 0.75
    assert res["latency_ms"] > 0


def test_predict_wet_scenario():
    payload = {
        "soil_moisture_percent": 48.0,
        "temperature_c": 21.0,
        "humidity_percent": 80.0,
        "rainfall_mm": 20.0,
        "field_zone": "South-Field-B"
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert res["prediction"] == 0
    assert res["action_code"] == "VALVE_CLOSED"
    assert res["irrigation_probability"] <= 0.25


def test_predict_validation_trap_out_of_bounds():
    # Soil moisture 150% is physically impossible
    payload = {
        "soil_moisture_percent": 150.0,
        "temperature_c": 25.0,
        "humidity_percent": 50.0,
        "rainfall_mm": 0.0
    }
    response = client.post("/api/predict", json=payload)
    # Pydantic or custom validation catches out-of-range values
    assert response.status_code in [400, 422]


def test_simulate_endpoint():
    payload = {
        "scenario": "Drought Stress (Critical Dry)",
        "count": 2
    }
    response = client.post("/api/simulate", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res["count"] == 2
    assert len(res["results"]) == 2


def test_telemetry_endpoint():
    response = client.get("/api/telemetry?limit=10")
    assert response.status_code == 200
    res = response.json()
    assert "total" in res
    assert "records" in res
    assert isinstance(res["records"], list)


def test_azure_status_endpoint():
    response = client.get("/api/azure-status")
    assert response.status_code == 200
    res = response.json()
    assert "is_configured" in res
    assert "model_file_exists" in res
    assert res["model_file_exists"] is True
