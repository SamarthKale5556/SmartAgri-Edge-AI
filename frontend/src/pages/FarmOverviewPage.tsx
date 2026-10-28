import React from 'react';
import { FarmScene } from '../components/farm3d/FarmScene';
import { useFarm } from '../context/FarmContext';
import {
  Droplets,
  Thermometer,
  CloudRain,
  Wind,
  CheckCircle2,
  AlertOctagon,
  Clock,
  Layers,
  ShieldCheck,
} from 'lucide-react';

export const FarmOverviewPage: React.FC = () => {
  const {
    latestPrediction,
    fieldZones,
    activeZoneId,
    setActiveZoneId,
  } = useFarm();

  const activeZone = fieldZones[activeZoneId];
  const pred = latestPrediction?.prediction ?? (activeZone.soilMoisture < 25 ? 1 : 0);
  const prob = latestPrediction?.irrigation_probability ?? activeZone.irrigationProbability;
  const latency = latestPrediction?.latency_ms ?? 58.4;
  const actionCode = latestPrediction?.action_code ?? (pred === 1 ? 'VALVE_OPEN' : 'VALVE_CLOSED');

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      <div>
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">
              Interactive 3D Field Environment
            </h3>
          </div>
          <span className="text-xs text-slate-400">
            Click any field sector to focus • Drag to orbit • Scroll to zoom
          </span>
        </div>
        <FarmScene />
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-slate-900/80 border border-white/10 shadow-lg relative overflow-hidden">
          <div className="flex justify-between items-start">
            <div>
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
                Soil Moisture
              </span>
              <span className="text-2xl font-black text-white mt-1 block">
                {activeZone.soilMoisture}%
              </span>
            </div>
            <div className="p-2 rounded-lg bg-emerald-950/80 border border-emerald-500/20 text-emerald-400">
              <Droplets className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-2 flex items-center text-xs">
            <span
              className={`font-semibold ${
                activeZone.soilMoisture < 20
                  ? 'text-rose-400'
                  : activeZone.soilMoisture > 40
                  ? 'text-sky-400'
                  : 'text-emerald-400'
              }`}
            >
              {activeZone.soilMoisture < 20
                ? 'Severe Deficit'
                : activeZone.soilMoisture > 40
                ? 'Saturated'
                : 'Optimal Field Capacity'}
            </span>
          </div>
          <div className="w-full bg-slate-800 h-1.5 rounded-full mt-2.5 overflow-hidden">
            <div
              className={`h-full transition-all duration-500 ${
                activeZone.soilMoisture < 20
                  ? 'bg-rose-500'
                  : activeZone.soilMoisture > 40
                  ? 'bg-sky-500'
                  : 'bg-emerald-500'
              }`}
              style={{ width: `${Math.min(100, (activeZone.soilMoisture / 60) * 100)}%` }}
            />
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/80 border border-white/10 shadow-lg">
          <div className="flex justify-between items-start">
            <div>
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
                Canopy Temp
              </span>
              <span className="text-2xl font-black text-white mt-1 block">
                {activeZone.temperature}°C
              </span>
            </div>
            <div className="p-2 rounded-lg bg-amber-950/80 border border-amber-500/20 text-amber-400">
              <Thermometer className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-2 text-xs text-slate-400">
            Evaporative driver: <span className="text-amber-300 font-semibold">{activeZone.temperature > 32 ? 'High Heat' : 'Moderate'}</span>
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/80 border border-white/10 shadow-lg">
          <div className="flex justify-between items-start">
            <div>
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
                Air Humidity
              </span>
              <span className="text-2xl font-black text-white mt-1 block">
                {activeZone.humidity}%
              </span>
            </div>
            <div className="p-2 rounded-lg bg-sky-950/80 border border-sky-500/20 text-sky-400">
              <Wind className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-2 text-xs text-slate-400">
            Vapor pressure deficit: <span className="text-sky-300 font-semibold">{activeZone.humidity < 35 ? 'Arid' : 'Normal'}</span>
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/80 border border-white/10 shadow-lg">
          <div className="flex justify-between items-start">
            <div>
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
                24h Rainfall
              </span>
              <span className="text-2xl font-black text-white mt-1 block">
                {activeZone.rainfall} mm
              </span>
            </div>
            <div className="p-2 rounded-lg bg-blue-950/80 border border-blue-500/20 text-blue-400">
              <CloudRain className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-2 text-xs text-slate-400">
            Suppression: <span className="text-blue-300 font-semibold">{activeZone.rainfall > 5 ? 'Active' : 'None'}</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 p-5 rounded-xl bg-slate-900/80 border border-white/10 shadow-xl flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-white/10 mb-4">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-emerald-400" />
                <h4 className="text-sm font-bold text-white uppercase tracking-wider">
                  Real-Time Edge ML Prediction
                </h4>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[11px] font-mono text-slate-400 flex items-center gap-1">
                  <Clock className="w-3.5 h-3.5 text-slate-400" />
                  {latency} ms
                </span>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-950 text-emerald-300 border border-emerald-800">
                  scikit-learn RF
                </span>
              </div>
            </div>

            {actionCode === 'VALVE_OPEN' ? (
              <div className="p-4 rounded-xl bg-gradient-to-r from-rose-950/80 to-amber-950/60 border border-rose-500/40 text-rose-200">
                <div className="flex items-center gap-3">
                  <AlertOctagon className="w-8 h-8 text-rose-400 shrink-0 animate-pulse" />
                  <div>
                    <h5 className="text-base font-extrabold text-white">
                      IRRIGATION RECOMMENDED • ACTUATOR: VALVE_OPEN
                    </h5>
                    <p className="text-xs text-rose-300 mt-0.5">
                      Critical root-zone moisture deficit detected under active atmospheric demand.
                      Solenoid valve opened for sector {activeZoneId}.
                    </p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="p-4 rounded-xl bg-gradient-to-r from-emerald-950/80 to-teal-950/60 border border-emerald-500/40 text-emerald-200">
                <div className="flex items-center gap-3">
                  <CheckCircle2 className="w-8 h-8 text-emerald-400 shrink-0" />
                  <div>
                    <h5 className="text-base font-extrabold text-white">
                      MOISTURE ADEQUATE • ACTUATOR: VALVE_CLOSED
                    </h5>
                    <p className="text-xs text-emerald-300 mt-0.5">
                      Soil water content is sufficient or recent precipitation has alleviated stress.
                      Water conserved.
                    </p>
                  </div>
                </div>
              </div>
            )}

            <div className="mt-5 space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Calculated Irrigation Probability:</span>
                <span className="font-bold text-white">{(prob * 100).toFixed(1)}%</span>
              </div>
              <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                <div
                  className={`h-full transition-all duration-700 ${
                    prob > 0.5 ? 'bg-gradient-to-r from-amber-500 to-rose-500' : 'bg-gradient-to-r from-teal-500 to-emerald-500'
                  }`}
                  style={{ width: `${Math.round(prob * 100)}%` }}
                />
              </div>
              <div className="flex justify-between text-[10px] text-slate-500">
                <span>0% (Conserve)</span>
                <span>Threshold: 50%</span>
                <span>100% (Irrigate)</span>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-white/5 mt-4 flex items-center justify-between text-xs text-slate-400">
            <span>Target: <strong>{activeZone.name}</strong></span>
            <span>Phenology: <strong>{activeZone.growthStage}</strong></span>
          </div>
        </div>

        <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 shadow-xl">
          <div className="flex items-center gap-2 pb-3 border-b border-white/10 mb-4">
            <Layers className="w-5 h-5 text-amber-400" />
            <h4 className="text-sm font-bold text-white uppercase tracking-wider">
              Field Sector Health Matrix
            </h4>
          </div>

          <div className="space-y-2.5">
            {Object.values(fieldZones).map((zone) => {
              const isSelected = zone.id === activeZoneId;
              return (
                <div
                  key={zone.id}
                  onClick={() => setActiveZoneId(zone.id)}
                  className={`p-2.5 rounded-lg border transition-all cursor-pointer flex items-center justify-between ${
                    isSelected
                      ? 'bg-emerald-950/60 border-emerald-500/50 shadow-md'
                      : 'bg-slate-800/40 border-white/5 hover:bg-slate-800/70'
                  }`}
                >
                  <div>
                    <div className="flex items-center gap-1.5">
                      <span
                        className={`w-2 h-2 rounded-full ${
                          zone.soilMoisture < 22
                            ? 'bg-rose-400'
                            : zone.soilMoisture > 40
                            ? 'bg-sky-400'
                            : 'bg-emerald-400'
                        }`}
                      />
                      <span className="text-xs font-bold text-white">{zone.name}</span>
                    </div>
                    <span className="text-[10px] text-slate-400 block mt-0.5">
                      Moisture: {zone.soilMoisture}% • Temp: {zone.temperature}°C
                    </span>
                  </div>

                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      zone.status === 'IRRIGATING'
                        ? 'bg-rose-950 text-rose-300 border border-rose-800'
                        : zone.status === 'DEFICIT'
                        ? 'bg-amber-950 text-amber-300 border border-amber-800'
                        : 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                    }`}
                  >
                    {zone.status}
                  </span>
                </div>
              );
            })}
          </div>

          <div className="mt-4 p-2.5 rounded bg-slate-800/60 border border-white/5 text-[11px] text-slate-400">
            💡 <strong>Tip:</strong> Click any sector above or on the 3D terrain to inspect localized sensor readings.
          </div>
        </div>
      </div>
    </div>
  );
};
