"""
simulate_iot.py - IoT Agro-Sensor Simulator
Smart Agriculture: Real-Time Irrigation Prediction at the IoT Edge

Simulates physical IoT field sensors (Soil Moisture, Temperature, Relative Humidity, Rain Gauge).
Can generate:
1. Single realistic readings with diurnal or environmental noise.
2. Named agricultural simulation scenarios (Drought Stress, Heavy Rain, Midday Heat, etc.).
3. Continuous telemetry streams (simulating periodic cron or timer-triggered sensor bursts).
4. Direct dispatch to the local EdgeInferenceEngine.
"""

import time
import random
import numpy as np
from typing import Dict, Any, List, Optional
from edge_inference import get_edge_engine, EdgeInferenceEngine


# Named agricultural scenarios for deterministic demonstration
SCENARIOS = {
    "Drought Stress (Critical Dry)": {
        "soil_moisture_range": (11.0, 17.5),
        "temperature_range": (33.0, 41.0),
        "humidity_range": (18.0, 32.0),
        "rainfall_range": (0.0, 0.0),
        "description": "High temperature, low humidity, severely depleted root-zone water."
    },
    "Adequate Post-Rain (Wet)": {
        "soil_moisture_range": (42.0, 56.0),
        "temperature_range": (18.0, 24.0),
        "humidity_range": (75.0, 92.0),
        "rainfall_range": (12.0, 32.0),
        "description": "Recent rainstorm, saturated soil, high relative humidity."
    },
    "Mild Morning (Temperate)": {
        "soil_moisture_range": (32.0, 39.0),
        "temperature_range": (20.0, 26.0),
        "humidity_range": (55.0, 70.0),
        "rainfall_range": (0.0, 1.5),
        "description": "Normal temperate morning conditions, moderate root moisture."
    },
    "Midday Heat Spike (Boundary)": {
        "soil_moisture_range": (24.0, 29.0),
        "temperature_range": (36.0, 42.0),
        "humidity_range": (25.0, 40.0),
        "rainfall_range": (0.0, 0.0),
        "description": "Transitional moisture zone subjected to severe evaporative heat demand."
    },
    "Sensor Fault / Corrupt Payload": {
        "soil_moisture_range": (135.0, 160.0),  # Intentionally out-of-bounds to test edge validation
        "temperature_range": (28.0, 32.0),
        "humidity_range": (50.0, 60.0),
        "rainfall_range": (0.0, 0.0),
        "description": "Simulates a faulty sensor sending an impossible >100% moisture reading."
    }
}


class IoTSensorSimulator:
    """Simulates an edge-connected agro-meteorological sensor cluster."""

    def __init__(self, node_id: str = "IOT-NODE-AGRI-01"):
        self.node_id = node_id

    def generate_reading(
        self,
        scenario_name: Optional[str] = None,
        custom_seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generates a single synthetic sensor reading payload.
        If scenario_name is provided, generates within that scenario's bounds.
        Otherwise generates a natural randomized ambient reading.
        """
        if custom_seed is not None:
            random.seed(custom_seed)
            np.random.seed(custom_seed)

        if scenario_name and scenario_name in SCENARIOS:
            sc = SCENARIOS[scenario_name]
            sm = round(random.uniform(*sc["soil_moisture_range"]), 1)
            temp = round(random.uniform(*sc["temperature_range"]), 1)
            hum = round(random.uniform(*sc["humidity_range"]), 1)
            rain = round(random.uniform(*sc["rainfall_range"]), 1)
        else:
            # Natural ambient stochastic generation
            temp = round(random.uniform(18.0, 38.0), 1)
            # Humidity roughly anti-correlated with temperature
            hum_base = 90.0 - 1.2 * (temp - 18.0)
            hum = round(float(np.clip(hum_base + random.uniform(-10.0, 10.0), 20.0, 95.0)), 1)
            # Rain occurrence probability ~ 20%
            rain = round(float(np.random.exponential(scale=4.0)) if random.random() < 0.22 else 0.0, 1)
            rain = min(rain, 40.0)
            # Soil moisture influenced by rainfall
            sm = round(float(np.clip(random.uniform(15.0, 45.0) + 0.5 * rain, 10.0, 58.0)), 1)

        payload = {
            "node_id": self.node_id,
            "soil_moisture_percent": sm,
            "temperature_c": temp,
            "humidity_percent": hum,
            "rainfall_mm": rain,
            "scenario": scenario_name or "Natural Stochastic Reading"
        }
        return payload

    def simulate_and_infer(
        self,
        engine: Optional[EdgeInferenceEngine] = None,
        scenario_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates a reading and executes edge inference immediately.
        Represents the physical pipeline: Sensor Reading -> Edge Inference -> Actuator Decision.
        """
        if engine is None:
            engine = get_edge_engine()

        reading = self.generate_reading(scenario_name=scenario_name)
        result = engine.predict(reading, record_history=True)
        return result

    def simulate_stream(
        self,
        num_readings: int = 5,
        engine: Optional[EdgeInferenceEngine] = None,
        delay_seconds: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Simulates a continuous stream of sensor telemetry payloads.
        """
        if engine is None:
            engine = get_edge_engine()

        results = []
        for i in range(num_readings):
            res = self.simulate_and_infer(engine)
            results.append(res)
            if delay_seconds > 0:
                time.sleep(delay_seconds)
        return results


if __name__ == "__main__":
    print("=====================================================")
    print("Simulating IoT Sensor Telemetry & Local Edge Dispatch")
    print("=====================================================")
    sim = IoTSensorSimulator()
    engine = get_edge_engine()

    for sc_name in SCENARIOS:
        print(f"\n--- Scenario: {sc_name} ---")
        outcome = sim.simulate_and_infer(engine, scenario_name=sc_name)
        if outcome["success"]:
            print(f"Reading: SM={outcome['reading']['soil_moisture_percent']}%, "
                  f"Temp={outcome['reading']['temperature_c']}°C, "
                  f"Hum={outcome['reading']['humidity_percent']}%, "
                  f"Rain={outcome['reading']['rainfall_mm']}mm")
            print(f"Decision: {outcome['recommendation']} [{outcome['action_code']}] "
                  f"(Prob: {outcome['irrigation_probability']:.2f}, Latency: {outcome['latency_ms']} ms)")
        else:
            print(f"Edge Validation Trap: {outcome['error']} (Status: {outcome['status']})")
