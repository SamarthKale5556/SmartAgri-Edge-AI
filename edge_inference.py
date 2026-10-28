"""
edge_inference.py - Local Edge Inference Service & Telemetry Storage
Smart Agriculture: Real-Time Irrigation Prediction at the IoT Edge

Key Responsibilities:
1. Loads and caches the serialized model pipeline locally (zero-cloud edge execution).
2. Performs strict physical boundary and type validation on incoming sensor telemetry.
3. Computes real-time inference latency (milliseconds).
4. Emits actionable edge control directives (e.g. VALVE_OPEN / VALVE_CLOSED).
5. Persists telemetry and inference outcomes in a lightweight SQLite edge database.
"""

import os
import time
import sqlite3
import joblib
import pandas as pd
from typing import Dict, Any, Tuple, Optional
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "irrigation_model.joblib")
DB_PATH = os.path.join(BASE_DIR, "data", "edge_telemetry.db")

# Physical sensor acceptable ranges
VALIDATION_RULES = {
    "soil_moisture_percent": {"min": 0.0, "max": 100.0, "unit": "%"},
    "temperature_c": {"min": -10.0, "max": 65.0, "unit": "°C"},
    "humidity_percent": {"min": 0.0, "max": 100.0, "unit": "%"},
    "rainfall_mm": {"min": 0.0, "max": 300.0, "unit": "mm"},
}


class EdgeInferenceEngine:
    """Edge inference runtime designed for low-latency in-situ processing."""

    def __init__(self, model_path: str = MODEL_PATH, db_path: str = DB_PATH):
        self.model_path = model_path
        self.db_path = db_path
        self.model = None
        self.load_time_ms = 0.0
        self._load_model()
        self._init_db()

    def _load_model(self):
        """Loads serialized model artifact into memory."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model file not found at '{self.model_path}'. "
                "Ensure train_model.py has been executed."
            )
        start_t = time.perf_counter()
        self.model = joblib.load(self.model_path)
        self.load_time_ms = round((time.perf_counter() - start_t) * 1000, 2)
        print(f"[EDGE ENGINE] Model loaded successfully in {self.load_time_ms} ms from {self.model_path}")

    def _init_db(self):
        """Initializes local SQLite database for edge telemetry logging."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS telemetry_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    soil_moisture REAL NOT NULL,
                    temperature REAL NOT NULL,
                    humidity REAL NOT NULL,
                    rainfall REAL NOT NULL,
                    prediction INTEGER NOT NULL,
                    recommendation TEXT NOT NULL,
                    action_code TEXT NOT NULL,
                    confidence_score REAL NOT NULL,
                    irrigation_probability REAL NOT NULL,
                    latency_ms REAL NOT NULL,
                    status TEXT NOT NULL
                )
            """)
            conn.commit()

    def validate_reading(self, reading: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validates incoming sensor readings against schema and physical plausibility bounds.
        Returns: (is_valid: bool, error_message: Optional[str])
        """
        required_fields = ["soil_moisture_percent", "temperature_c", "humidity_percent", "rainfall_mm"]
        for field in required_fields:
            if field not in reading:
                return False, f"Missing required telemetry key: '{field}'"
            val = reading[field]
            if val is None:
                return False, f"Telemetry field '{field}' cannot be None"
            try:
                num_val = float(val)
            except (ValueError, TypeError):
                return False, f"Field '{field}' must be numeric, received: {type(val).__name__} ({val})"

            rule = VALIDATION_RULES[field]
            if not (rule["min"] <= num_val <= rule["max"]):
                return (
                    False,
                    f"Out of physical bounds for '{field}': {num_val}{rule['unit']} "
                    f"(Permitted: {rule['min']} to {rule['max']}{rule['unit']})"
                )

        return True, None

    def predict(self, reading: Dict[str, Any], record_history: bool = True) -> Dict[str, Any]:
        """
        Executes edge inference on a single sensor payload.
        Ensures local-only execution without requiring cloud network round-trips.
        """
        is_valid, error_msg = self.validate_reading(reading)
        if not is_valid:
            return {
                "success": False,
                "error": error_msg,
                "reading": reading,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "VALIDATION_FAILED"
            }

        start_t = time.perf_counter()

        features = [
            float(reading["soil_moisture_percent"]),
            float(reading["temperature_c"]),
            float(reading["humidity_percent"]),
            float(reading["rainfall_mm"]),
        ]

        df_in = pd.DataFrame([features], columns=[
            "soil_moisture_percent", "temperature_c", "humidity_percent", "rainfall_mm"
        ])

        # Local inference execution
        pred = int(self.model.predict(df_in)[0])
        probabilities = self.model.predict_proba(df_in)[0]
        prob_irrigation = float(probabilities[1])
        prob_no_irrigation = float(probabilities[0])

        latency_ms = round((time.perf_counter() - start_t) * 1000, 3)

        if pred == 1:
            recommendation = "Irrigation Recommended (Moisture Deficit Detected)"
            action_code = "VALVE_OPEN"
            confidence = prob_irrigation
        else:
            recommendation = "Moisture Adequate (No Irrigation Needed)"
            action_code = "VALVE_CLOSED"
            confidence = prob_no_irrigation

        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        result = {
            "success": True,
            "timestamp": timestamp_str,
            "reading": reading,
            "prediction": pred,
            "recommendation": recommendation,
            "action_code": action_code,
            "confidence_score": round(confidence, 4),
            "irrigation_probability": round(prob_irrigation, 4),
            "latency_ms": latency_ms,
            "status": "INFERENCE_SUCCESS"
        }

        if record_history:
            self._save_telemetry(result)

        return result

    def _save_telemetry(self, res: Dict[str, Any]):
        """Persists inference record into SQLite."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                r = res["reading"]
                cursor.execute("""
                    INSERT INTO telemetry_history (
                        timestamp, soil_moisture, temperature, humidity, rainfall,
                        prediction, recommendation, action_code, confidence_score,
                        irrigation_probability, latency_ms, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    res["timestamp"],
                    float(r["soil_moisture_percent"]),
                    float(r["temperature_c"]),
                    float(r["humidity_percent"]),
                    float(r["rainfall_mm"]),
                    res["prediction"],
                    res["recommendation"],
                    res["action_code"],
                    res["confidence_score"],
                    res["irrigation_probability"],
                    res["latency_ms"],
                    res["status"]
                ))
                conn.commit()
        except Exception as e:
            print(f"[EDGE WARNING] Failed to persist telemetry: {e}")

    def get_history_df(self, limit: int = 100) -> pd.DataFrame:
        """Retrieves recent telemetry and predictions as a pandas DataFrame."""
        if not os.path.exists(self.db_path):
            return pd.DataFrame()
        with sqlite3.connect(self.db_path) as conn:
            query = f"SELECT * FROM telemetry_history ORDER BY id DESC LIMIT {limit}"
            df = pd.read_sql_query(query, conn)
        return df

    def clear_history(self):
        """Clears SQLite telemetry table."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM telemetry_history")
            conn.commit()


# Singleton edge engine instance for easy reuse
_engine_instance: Optional[EdgeInferenceEngine] = None


def get_edge_engine() -> EdgeInferenceEngine:
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = EdgeInferenceEngine()
    return _engine_instance


if __name__ == "__main__":
    print("[TEST] Running local edge inference engine sanity test...")
    engine = EdgeInferenceEngine()

    sample_dry = {
        "soil_moisture_percent": 14.5,
        "temperature_c": 36.2,
        "humidity_percent": 24.0,
        "rainfall_mm": 0.0
    }
    res1 = engine.predict(sample_dry)
    print(f"Sample 1 (Drought/Hot): Pred={res1['prediction']}, Action={res1['action_code']}, "
          f"Prob={res1['irrigation_probability']}, Latency={res1['latency_ms']} ms")

    sample_wet = {
        "soil_moisture_percent": 48.0,
        "temperature_c": 22.0,
        "humidity_percent": 82.0,
        "rainfall_mm": 18.5
    }
    res2 = engine.predict(sample_wet)
    print(f"Sample 2 (Wet/Rain)    : Pred={res2['prediction']}, Action={res2['action_code']}, "
          f"Prob={res2['irrigation_probability']}, Latency={res2['latency_ms']} ms")

    sample_invalid = {
        "soil_moisture_percent": 150.0,
        "temperature_c": 30.0,
        "humidity_percent": 50.0,
        "rainfall_mm": 0.0
    }
    res3 = engine.predict(sample_invalid)
    print(f"Sample 3 (Invalid)     : Success={res3['success']}, Error='{res3.get('error')}'")
