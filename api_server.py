"""
api_server.py - FastAPI Backend Service for AgriSense Edge AI
Connects the React 3D Smart Agriculture Frontend to the Real Python ML Edge Pipeline.

Exposes:
- GET  /api/health
- GET  /api/model-info
- GET  /api/metrics
- POST /api/predict
- POST /api/simulate
- GET  /api/telemetry
- GET  /api/export
- GET  /api/azure-status
- POST /api/azure-register
- POST /api/reset-simulation
"""

import os
import io
import json
import sqlite3
import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from edge_inference import get_edge_engine, MODEL_PATH, DB_PATH, VALIDATION_RULES
from simulate_iot import IoTSensorSimulator, SCENARIOS
from register_azure_model import check_azure_status, register_model_to_azure

app = FastAPI(
    title="AgriSense Edge AI - Smart Agriculture API",
    description="Real-Time IoT Edge ML Inference and Farm Telemetry Service",
    version="2.0.0"
)

# CORS setup for local React Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = get_edge_engine()
simulator = IoTSensorSimulator()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
METRICS_PATH = os.path.join(BASE_DIR, "outputs", "evaluation_metrics.json")
ASSUMPTIONS_PATH = os.path.join(BASE_DIR, "outputs", "dataset_assumptions.json")


# Pydantic Schemas
class SensorReadingInput(BaseModel):
    soil_moisture_percent: float = Field(..., ge=0.0, le=100.0, description="Volumetric soil moisture percentage (0-100%)")
    temperature_c: float = Field(..., ge=-10.0, le=65.0, description="Ambient air temperature in Celsius (-10 to 65°C)")
    humidity_percent: float = Field(..., ge=0.0, le=100.0, description="Relative air humidity percentage (0-100%)")
    rainfall_mm: float = Field(..., ge=0.0, le=300.0, description="Precipitation in millimeters (0-300mm)")
    field_zone: Optional[str] = Field("North-Field-A", description="Identifier of the field sector/zone")


class SimulationRequest(BaseModel):
    scenario: Optional[str] = Field(None, description="Preset scenario name, e.g., 'Drought Stress (Critical Dry)'")
    count: Optional[int] = Field(1, ge=1, le=20, description="Number of packets to simulate (1-20)")


@app.get("/api/health")
def get_health():
    """Health check endpoint indicating model state and workspace identity."""
    model_loaded = engine.model is not None
    return {
        "status": "healthy" if model_loaded else "degraded",
        "system": "AgriSense Edge AI",
        "workspace": "Samarth Kale's Workspace",
        "edge_model_loaded": model_loaded,
        "edge_model_active": model_loaded,
        "engine_load_time_ms": engine.load_time_ms,
        "db_connected": os.path.exists(DB_PATH),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/model-info")
def get_model_info():
    """Returns technical details and physical metadata of the deployed edge model."""
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(status_code=404, detail="Model artifact missing. Run train_model.py.")

    stat = os.stat(MODEL_PATH)
    return {
        "model_name": "RandomForest_Irrigation_Classifier",
        "version": "1.0.0",
        "framework": "scikit-learn",
        "pipeline_stages": ["StandardScaler", "RandomForestClassifier"],
        "artifact_path": MODEL_PATH,
        "file_size_bytes": stat.st_size,
        "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "input_features": [
            {"name": "soil_moisture_percent", "type": "float", "unit": "%", "acceptable_range": [0.0, 100.0]},
            {"name": "temperature_c", "type": "float", "unit": "°C", "acceptable_range": [-10.0, 65.0]},
            {"name": "humidity_percent", "type": "float", "unit": "%", "acceptable_range": [0.0, 100.0]},
            {"name": "rainfall_mm", "type": "float", "unit": "mm", "acceptable_range": [0.0, 300.0]}
        ],
        "output_classes": {
            0: "Moisture Adequate (VALVE_CLOSED)",
            1: "Irrigation Recommended (VALVE_OPEN)"
        }
    }


@app.get("/api/metrics")
def get_evaluation_metrics():
    """Returns held-out test evaluation metrics and dataset generation assumptions."""
    if not os.path.exists(METRICS_PATH):
        raise HTTPException(status_code=404, detail="Metrics file missing. Run train_model.py.")

    with open(METRICS_PATH, "r") as f:
        metrics = json.load(f)

    assumptions = {}
    if os.path.exists(ASSUMPTIONS_PATH):
        with open(ASSUMPTIONS_PATH, "r") as f:
            assumptions = json.load(f)

    return {
        "metrics": metrics,
        "assumptions": assumptions,
        "is_synthetic": True,
        "disclaimer": (
            "Model evaluated on 500 held-out test samples from a reproducible synthetic dataset (seed=42). "
            "High test scores demonstrate alignment with physical-heuristic equations, not in-situ field measurement."
        )
    }


@app.post("/api/predict")
def predict_irrigation(payload: SensorReadingInput):
    """
    Executes real scikit-learn edge inference on incoming sensor values.
    Persists decision to SQLite and emits real latency.
    """
    reading_dict = {
        "soil_moisture_percent": payload.soil_moisture_percent,
        "temperature_c": payload.temperature_c,
        "humidity_percent": payload.humidity_percent,
        "rainfall_mm": payload.rainfall_mm,
        "field_zone": payload.field_zone
    }

    result = engine.predict(reading_dict, record_history=True)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error", "Validation error"))

    return result


@app.post("/api/simulate")
def run_simulation(req: SimulationRequest):
    """
    Simulates single or streaming sensor telemetry packets and executes edge prediction.
    """
    if req.count == 1:
        res = simulator.simulate_and_infer(engine, scenario_name=req.scenario)
        return {"count": 1, "results": [res]}
    else:
        results = []
        for _ in range(req.count):
            res = simulator.simulate_and_infer(engine, scenario_name=req.scenario)
            results.append(res)
        return {"count": req.count, "results": results}


@app.get("/api/telemetry")
def get_telemetry(limit: int = Query(100, ge=1, le=500)):
    """Fetches recent telemetry and prediction logs from the SQLite edge database."""
    df = engine.get_history_df(limit=limit)
    if df.empty:
        return {"total": 0, "records": []}
    
    records = df.to_dict(orient="records")
    return {"total": len(records), "records": records}


@app.get("/api/export")
def export_telemetry_csv():
    """Generates a downloadable CSV stream of all edge telemetry logs."""
    df = engine.get_history_df(limit=1000)
    output = io.StringIO()
    df.to_csv(output, index=False)
    
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=agrisense_telemetry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
    )


@app.get("/api/azure-status")
def get_azure_status():
    """Returns the true connection and model registration status for Azure Machine Learning."""
    return check_azure_status()


@app.post("/api/azure-register")
def trigger_azure_register():
    """Attempts Azure ML model registration using SDK v2 or returns diagnostic guidance."""
    result = register_model_to_azure()
    return result


@app.post("/api/reset-simulation")
def reset_simulation():
    """Clears the SQLite telemetry log to reset the live simulation environment."""
    engine.clear_history()
    # Insert one default baseline reading for immediate clean visualization
    baseline = {
        "soil_moisture_percent": 34.0,
        "temperature_c": 24.5,
        "humidity_percent": 60.0,
        "rainfall_mm": 0.0,
        "scenario": "Baseline Post-Reset"
    }
    engine.predict(baseline, record_history=True)
    return {"message": "Simulation reset successfully", "baseline_created": True}


if __name__ == "__main__":
    import uvicorn
    print("[SERVER] Starting AgriSense FastAPI Server on http://localhost:8000...")
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=False)
