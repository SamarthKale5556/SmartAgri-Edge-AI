import React, { useState } from 'react';
import { useFarm } from '../context/FarmContext';
import {
  Sliders,
  RotateCcw,
  Waves,
  Zap,
  AlertTriangle,
  CheckCircle2,
  Cpu,
  Layers,
  Activity,
} from 'lucide-react';

export const LiveSimulationPage: React.FC = () => {
  const {
    activeZoneId,
    fieldZones,
    runPrediction,
    runSimulation,
    resetFarm,
    latestPrediction,
    isLoading,
  } = useFarm();

  const activeZone = fieldZones[activeZoneId];

  const [soilMoisture, setSoilMoisture] = useState<number>(activeZone?.soilMoisture ?? 22.0);
  const [temperature, setTemperature] = useState<number>(activeZone?.temperature ?? 32.0);
  const [humidity, setHumidity] = useState<number>(activeZone?.humidity ?? 40.0);
  const [rainfall, setRainfall] = useState<number>(activeZone?.rainfall ?? 0.0);
  const [selectedPreset, setSelectedPreset] = useState<string>('Drought Stress (Critical Dry)');
  const [feedbackMsg, setFeedbackMsg] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  const presets: Record<string, { sm: number; temp: number; hum: number; rain: number; desc: string }> = {
    'Drought Stress (Critical Dry)': {
      sm: 13.5,
      temp: 37.8,
      hum: 22.0,
      rain: 0.0,
      desc: 'Severe root-zone water depletion under blistering atmospheric vapor pressure deficit.'
    },
    'Adequate Post-Rain (Wet)': {
      sm: 48.0,
      temp: 20.5,
      hum: 82.0,
      rain: 22.0,
      desc: 'Recent precipitation event; saturated soil canopy. High relative humidity.'
    },
    'Mild Morning (Temperate)': {
      sm: 35.0,
      temp: 24.0,
      hum: 60.0,
      rain: 0.5,
      desc: 'Balanced diurnal baseline with low evaporative demand.'
    },
    'Midday Heat Spike (Boundary)': {
      sm: 26.5,
      temp: 39.5,
      hum: 30.0,
      rain: 0.0,
      desc: 'Borderline moisture zone subject to rapid thermal moisture draw.'
    },
    'Sensor Malfunction / Fault Trap': {
      sm: 145.0,
      temp: 28.0,
      hum: 50.0,
      rain: 0.0,
      desc: 'Intentionally corrupted analog payload (>100%) to test edge validation traps.'
    }
  };

  const handleApplyPreset = (presetKey: string) => {
    setSelectedPreset(presetKey);
    const p = presets[presetKey];
    setSoilMoisture(p.sm);
    setTemperature(p.temp);
    setHumidity(p.hum);
    setRainfall(p.rain);
    setFeedbackMsg({ text: `Preset loaded: ${presetKey}`, type: 'success' });
  };

  const handleRunCustomPrediction = async () => {
    setFeedbackMsg(null);
    try {
      const res = await runPrediction({
        soil_moisture_percent: soilMoisture,
        temperature_c: temperature,
        humidity_percent: humidity,
        rainfall_mm: rainfall,
        field_zone: activeZoneId,
      });

      setFeedbackMsg({
        text: `Inference Success: ${res.recommendation} (Latency: ${res.latency_ms} ms)`,
        type: 'success',
      });
    } catch (e: any) {
      setFeedbackMsg({
        text: `Edge Trap Triggered: ${e.message}`,
        type: 'error',
      });
    }
  };

  const handleSimulateBatch = async (count: number) => {
    setFeedbackMsg(null);
    try {
      await runSimulation(selectedPreset, count);
      setFeedbackMsg({
        text: `Simulated ${count} telemetry packets successfully and recorded to SQLite.`,
        type: 'success',
      });
    } catch (e: any) {
      setFeedbackMsg({ text: `Simulation error: ${e.message}`, type: 'error' });
    }
  };

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      <div className="p-5 rounded-xl bg-gradient-to-r from-emerald-950/70 via-slate-900 to-slate-900 border border-emerald-500/20 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Activity className="w-5 h-5 text-emerald-400" />
              Live Farm Telemetry Simulator & Actuator Testing
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Inject synthetic environmental stimuli, run real in-situ scikit-learn inference, and verify actuator directives.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={() => handleSimulateBatch(1)}
              disabled={isLoading}
              className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold shadow-lg transition-all"
            >
              <Zap className="w-3.5 h-3.5" />
              <span>Generate Single Reading</span>
            </button>

            <button
              onClick={() => handleSimulateBatch(10)}
              disabled={isLoading}
              className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-teal-600 hover:bg-teal-500 text-white text-xs font-semibold shadow-lg transition-all"
            >
              <Waves className="w-3.5 h-3.5" />
              <span>Simulate 10 Readings</span>
            </button>

            <button
              onClick={resetFarm}
              disabled={isLoading}
              className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium border border-white/10 transition-all"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reset Simulation</span>
            </button>
          </div>
        </div>
      </div>

      {feedbackMsg && (
        <div
          className={`p-3 rounded-lg border text-xs font-medium flex items-center gap-2 ${
            feedbackMsg.type === 'success'
              ? 'bg-emerald-950/70 border-emerald-500/40 text-emerald-200'
              : 'bg-rose-950/70 border-rose-500/40 text-rose-200'
          }`}
        >
          {feedbackMsg.type === 'success' ? (
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          ) : (
            <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0" />
          )}
          <span>{feedbackMsg.text}</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 shadow-xl space-y-3">
          <div className="flex items-center gap-2 pb-2 border-b border-white/10">
            <Layers className="w-4 h-4 text-emerald-400" />
            <h4 className="text-xs font-bold text-white uppercase tracking-wider">
              Agricultural Scenario Presets
            </h4>
          </div>

          <div className="space-y-2">
            {Object.entries(presets).map(([key, data]) => (
              <div
                key={key}
                onClick={() => handleApplyPreset(key)}
                className={`p-3 rounded-lg border text-xs transition-all cursor-pointer ${
                  selectedPreset === key
                    ? 'bg-emerald-950/80 border-emerald-500/50 shadow-md'
                    : 'bg-slate-800/40 border-white/5 hover:bg-slate-800/70'
                }`}
              >
                <div className="flex items-center justify-between font-bold text-white">
                  <span>{key}</span>
                  <span className="text-[10px] text-emerald-400 font-mono">
                    SM: {data.sm}%
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 mt-1">{data.desc}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="lg:col-span-2 p-5 rounded-xl bg-slate-900/80 border border-white/10 shadow-xl space-y-5">
          <div className="flex items-center justify-between pb-3 border-b border-white/10">
            <div className="flex items-center gap-2">
              <Sliders className="w-4 h-4 text-amber-400" />
              <h4 className="text-xs font-bold text-white uppercase tracking-wider">
                Precision Sensor Calibrator (Manual Input Override)
              </h4>
            </div>
            <span className="text-[11px] text-slate-400">
              Active Zone: <strong className="text-white">{activeZoneId}</strong>
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-slate-400 font-medium">Volumetric Soil Moisture:</span>
                <span className="font-mono font-bold text-emerald-400">{soilMoisture}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                step="0.5"
                value={soilMoisture}
                onChange={(e) => setSoilMoisture(parseFloat(e.target.value))}
                className="w-full accent-emerald-500 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-500">
                <span>0% (Wilting Point)</span>
                <span>Critical: 20%</span>
                <span>100% (Flooded)</span>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-slate-400 font-medium">Canopy Temperature:</span>
                <span className="font-mono font-bold text-amber-400">{temperature}°C</span>
              </div>
              <input
                type="range"
                min="-5"
                max="60"
                step="0.5"
                value={temperature}
                onChange={(e) => setTemperature(parseFloat(e.target.value))}
                className="w-full accent-amber-500 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-500">
                <span>-5°C (Frost)</span>
                <span>Optimal: 25°C</span>
                <span>60°C (Extreme Heat)</span>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-slate-400 font-medium">Relative Air Humidity:</span>
                <span className="font-mono font-bold text-sky-400">{humidity}%</span>
              </div>
              <input
                type="range"
                min="5"
                max="100"
                step="0.5"
                value={humidity}
                onChange={(e) => setHumidity(parseFloat(e.target.value))}
                className="w-full accent-sky-500 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-500">
                <span>5% (Arid)</span>
                <span>Normal: 50%</span>
                <span>100% (Fog / Saturated)</span>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-slate-400 font-medium">Recent Rainfall:</span>
                <span className="font-mono font-bold text-blue-400">{rainfall} mm</span>
              </div>
              <input
                type="range"
                min="0"
                max="80"
                step="0.5"
                value={rainfall}
                onChange={(e) => setRainfall(parseFloat(e.target.value))}
                className="w-full accent-blue-500 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-500">
                <span>0 mm</span>
                <span>Suppression: &gt;8 mm</span>
                <span>80 mm (Storm)</span>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-white/10 flex items-center justify-between">
            <span className="text-xs text-slate-400">
              Payload ready for edge ML pipeline dispatch
            </span>
            <button
              onClick={handleRunCustomPrediction}
              disabled={isLoading}
              className="flex items-center gap-2 px-6 py-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white text-xs font-bold shadow-lg shadow-emerald-950/50 cursor-pointer transition-all"
            >
              <Cpu className="w-4 h-4" />
              <span>{isLoading ? 'Executing Edge Inference...' : 'Dispatch Payload to Edge Model'}</span>
            </button>
          </div>

          {latestPrediction && (
            <div className="mt-4 p-4 rounded-xl bg-slate-950 border border-white/10 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-white uppercase tracking-wider">
                  Latest Inference Outcome
                </span>
                <span className="text-[11px] font-mono text-emerald-400">
                  Latency: {latestPrediction.latency_ms} ms
                </span>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
                <div className="p-2 rounded bg-slate-900 border border-white/5">
                  <span className="text-[10px] text-slate-400 block">Class Decision</span>
                  <span className="font-bold text-white text-sm">
                    {latestPrediction.prediction === 1 ? 'Irrigate (1)' : 'Conserve (0)'}
                  </span>
                </div>
                <div className="p-2 rounded bg-slate-900 border border-white/5">
                  <span className="text-[10px] text-slate-400 block">Actuator State</span>
                  <span
                    className={`font-bold text-sm ${
                      latestPrediction.action_code === 'VALVE_OPEN' ? 'text-rose-400' : 'text-emerald-400'
                    }`}
                  >
                    {latestPrediction.action_code}
                  </span>
                </div>
                <div className="p-2 rounded bg-slate-900 border border-white/5">
                  <span className="text-[10px] text-slate-400 block">Confidence</span>
                  <span className="font-bold text-white text-sm">
                    {(latestPrediction.confidence_score * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="p-2 rounded bg-slate-900 border border-white/5">
                  <span className="text-[10px] text-slate-400 block">Irrigation Probability</span>
                  <span className="font-bold text-amber-400 text-sm">
                    {(latestPrediction.irrigation_probability * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
