import React from 'react';
import {
  ArrowRight,
  ShieldAlert,
  Compass,
} from 'lucide-react';

export const ProjectInfoPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6 max-w-5xl mx-auto">
      <div className="p-6 rounded-xl bg-gradient-to-r from-emerald-950/80 via-slate-900 to-slate-900 border border-emerald-500/20 shadow-xl flex items-center justify-between">
        <div>
          <span className="text-[11px] font-bold text-emerald-400 uppercase tracking-wider block mb-1">
            PBA-2 Practical Project Specification
          </span>
          <h2 className="text-xl font-extrabold text-white">
            Smart Agriculture: Real-Time Irrigation Prediction at the IoT Edge
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Autonomous In-Situ ML Edge System with Interactive 3D Farm Digital Twin
          </p>
        </div>

        <div className="hidden sm:flex items-center gap-3 px-3 py-2 rounded-xl bg-slate-800/60 border border-white/10">
          <div className="w-9 h-9 rounded-full bg-emerald-700 flex items-center justify-center font-bold text-white text-sm">
            SK
          </div>
          <div className="text-right">
            <span className="text-xs font-bold text-white block">Samarth Kale</span>
            <span className="text-[10px] text-emerald-400 block">Lead Engineer / Author</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 shadow-lg space-y-2">
          <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider">
            1. Problem Statement
          </h4>
          <p className="text-xs text-slate-300 leading-relaxed">
            Agricultural fields require precise, timely water delivery. Over-watering depletes aquifers and leaches vital nutrients, while under-watering induces severe moisture stress and crop yield collapse. Remote rural farms lack reliable internet connectivity, rendering cloud-dependent inference fragile.
          </p>
        </div>

        <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 shadow-lg space-y-2">
          <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider">
            2. Edge ML Objective
          </h4>
          <p className="text-xs text-slate-300 leading-relaxed">
            Deploy a lightweight, low-power machine learning classifier locally on an edge gateway node. The model evaluates multi-sensor telemetry (soil moisture, temperature, humidity, rainfall) in under 100 milliseconds without internet dependence, issuing immediate actuator commands (<code className="text-emerald-400">VALVE_OPEN</code> / <code className="text-emerald-400">VALVE_CLOSED</code>).
          </p>
        </div>
      </div>

      <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 shadow-xl space-y-4">
        <h4 className="text-xs font-bold text-white uppercase tracking-wider">
          3. End-to-End Operational Data Flow
        </h4>

        <div className="flex flex-col md:flex-row items-center justify-between gap-3 text-center text-xs">
          <div className="p-3 rounded-lg bg-slate-800/80 border border-white/10 w-full">
            <span className="text-[10px] text-slate-400 block uppercase">Step 1</span>
            <strong className="text-white block mt-0.5">Simulated IoT Sensors</strong>
            <span className="text-[10px] text-slate-400">Moisture, Temp, Humidity, Rain</span>
          </div>

          <ArrowRight className="w-5 h-5 text-emerald-400 shrink-0 hidden md:block" />

          <div className="p-3 rounded-lg bg-slate-800/80 border border-white/10 w-full">
            <span className="text-[10px] text-slate-400 block uppercase">Step 2</span>
            <strong className="text-white block mt-0.5">FastAPI Backend</strong>
            <span className="text-[10px] text-slate-400">Pydantic Validation Traps</span>
          </div>

          <ArrowRight className="w-5 h-5 text-emerald-400 shrink-0 hidden md:block" />

          <div className="p-3 rounded-lg bg-emerald-950/80 border border-emerald-500/30 w-full">
            <span className="text-[10px] text-emerald-400 block uppercase">Step 3</span>
            <strong className="text-white block mt-0.5">Local ML Model</strong>
            <span className="text-[10px] text-emerald-300">RandomForest (&lt; 75 ms)</span>
          </div>

          <ArrowRight className="w-5 h-5 text-emerald-400 shrink-0 hidden md:block" />

          <div className="p-3 rounded-lg bg-slate-800/80 border border-white/10 w-full">
            <span className="text-[10px] text-slate-400 block uppercase">Step 4</span>
            <strong className="text-white block mt-0.5">SQLite & Actuator</strong>
            <span className="text-[10px] text-slate-400">VALVE_OPEN / CLOSED</span>
          </div>

          <ArrowRight className="w-5 h-5 text-emerald-400 shrink-0 hidden md:block" />

          <div className="p-3 rounded-lg bg-slate-800/80 border border-white/10 w-full">
            <span className="text-[10px] text-slate-400 block uppercase">Step 5</span>
            <strong className="text-white block mt-0.5">3D React Twin</strong>
            <span className="text-[10px] text-slate-400">Three.js + Live HUD</span>
          </div>
        </div>

        <div className="p-3 rounded-lg bg-slate-950 border border-white/5 text-[11px] text-slate-400">
          <strong>Separate Lifecycle:</strong> Azure Machine Learning model registration operates asynchronously as an MLOps lifecycle step for seasonal retraining, completely separated from the live real-time valve control loop.
        </div>
      </div>

      <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 shadow-xl space-y-3">
        <h4 className="text-xs font-bold text-white uppercase tracking-wider">
          4. Complete Technology Stack
        </h4>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
          <div className="p-3 rounded-lg bg-slate-800/50 border border-white/5">
            <span className="text-[10px] text-slate-400 block">3D Graphics</span>
            <span className="font-bold text-white">Three.js / R3F</span>
          </div>
          <div className="p-3 rounded-lg bg-slate-800/50 border border-white/5">
            <span className="text-[10px] text-slate-400 block">Frontend Framework</span>
            <span className="font-bold text-white">React 19 + TypeScript</span>
          </div>
          <div className="p-3 rounded-lg bg-slate-800/50 border border-white/5">
            <span className="text-[10px] text-slate-400 block">Styling</span>
            <span className="font-bold text-white">Tailwind CSS v4</span>
          </div>
          <div className="p-3 rounded-lg bg-slate-800/50 border border-white/5">
            <span className="text-[10px] text-slate-400 block">Charts</span>
            <span className="font-bold text-white">Recharts / Plotly</span>
          </div>
          <div className="p-3 rounded-lg bg-slate-800/50 border border-white/5">
            <span className="text-[10px] text-slate-400 block">Backend Server</span>
            <span className="font-bold text-white">FastAPI / Uvicorn</span>
          </div>
          <div className="p-3 rounded-lg bg-slate-800/50 border border-white/5">
            <span className="text-[10px] text-slate-400 block">ML Engine</span>
            <span className="font-bold text-white">scikit-learn Pipeline</span>
          </div>
          <div className="p-3 rounded-lg bg-slate-800/50 border border-white/5">
            <span className="text-[10px] text-slate-400 block">Embedded DB</span>
            <span className="font-bold text-white">SQLite3 (Local)</span>
          </div>
          <div className="p-3 rounded-lg bg-slate-800/50 border border-white/5">
            <span className="text-[10px] text-slate-400 block">Cloud MLOps</span>
            <span className="font-bold text-white">Azure ML SDK v2</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-5 rounded-xl bg-slate-900/80 border border-amber-500/20 shadow-lg space-y-2">
          <div className="flex items-center gap-2 text-amber-400">
            <ShieldAlert className="w-4 h-4" />
            <h4 className="text-xs font-bold uppercase tracking-wider">Current Limitations</h4>
          </div>
          <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside">
            <li>The dataset is synthetic (seed=42) and reflects mathematical simulation rules rather than physical farm soils.</li>
            <li>Sensors and valves are simulated locally; no physical LoRaWAN hardware or solenoid relays are attached.</li>
            <li>The crop coefficient is static across days instead of dynamically tracking vegetative stages.</li>
          </ul>
        </div>

        <div className="p-5 rounded-xl bg-slate-900/80 border border-emerald-500/20 shadow-lg space-y-2">
          <div className="flex items-center gap-2 text-emerald-400">
            <Compass className="w-4 h-4" />
            <h4 className="text-xs font-bold uppercase tracking-wider">Future Scope</h4>
          </div>
          <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside">
            <li>LoRaWAN multi-node radio gateways with ChirpStack MQTT ingestion.</li>
            <li>Multi-depth moisture profiling (10cm, 30cm, 60cm) to detect percolation.</li>
            <li>Model quantization via TinyML / TF-Lite for microcontroller deployment on ESP32.</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
