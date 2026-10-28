import React, { useState } from 'react';
import {
  Sun,
  RotateCcw,
  Bell,
  Cpu,
  X,
} from 'lucide-react';
import { useFarm } from '../../context/FarmContext';

interface TopBarProps {
  title: string;
  description: string;
}

export const TopBar: React.FC<TopBarProps> = ({ title, description }) => {
  const {
    simulatedWeather,
    notifications,
    runPrediction,
    resetFarm,
    fieldZones,
    activeZoneId,
    isLoading,
  } = useFarm();
  const [showNotifs, setShowNotifs] = useState(false);
  const [showResetConfirm, setShowResetConfirm] = useState(false);

  const activeZone = fieldZones[activeZoneId];

  const handleQuickPrediction = async () => {
    if (!activeZone) return;
    await runPrediction({
      soil_moisture_percent: activeZone.soilMoisture,
      temperature_c: activeZone.temperature,
      humidity_percent: activeZone.humidity,
      rainfall_mm: activeZone.rainfall,
      field_zone: activeZoneId,
    });
  };

  return (
    <header className="h-16 bg-[#0d1422]/90 border-b border-white/10 px-6 flex items-center justify-between sticky top-0 z-30 backdrop-blur-md">
      <div>
        <h2 className="text-base font-bold text-white tracking-tight">{title}</h2>
        <p className="text-xs text-slate-400">{description}</p>
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden lg:flex items-center gap-2.5 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-white/5 text-xs text-slate-300">
          <Sun className="w-4 h-4 text-amber-400" />
          <span>
            Simulated: <strong className="text-white">{simulatedWeather.temp}°C</strong> •{' '}
            <strong className="text-white">{simulatedWeather.humidity}% RH</strong> •{' '}
            <span className="text-amber-300 font-medium">{simulatedWeather.evaporationRisk} Evaporation</span>
          </span>
        </div>

        <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-emerald-950/60 border border-emerald-500/20 text-[11px] font-medium text-emerald-300">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping" />
          <span>Local Edge Mode</span>
        </div>

        <div className="relative">
          <button
            onClick={() => setShowNotifs(!showNotifs)}
            className="p-2 rounded-lg bg-slate-800/60 hover:bg-slate-700/60 text-slate-300 border border-white/10 transition-colors relative"
            title="Telemetry & Valve Alerts"
          >
            <Bell className="w-4 h-4" />
            {notifications.some((n) => n.type === 'alert') && (
              <span className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse" />
            )}
          </button>

          {showNotifs && (
            <div className="absolute right-0 mt-2 w-80 bg-slate-900 border border-white/10 rounded-xl shadow-2xl p-3 z-50 text-xs">
              <div className="flex items-center justify-between pb-2 border-b border-white/10 mb-2">
                <span className="font-bold text-white">Event & Actuator Log</span>
                <button onClick={() => setShowNotifs(false)} className="text-slate-400 hover:text-white">
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>
              <div className="max-h-60 overflow-y-auto space-y-2">
                {notifications.map((n) => (
                  <div
                    key={n.id}
                    className={`p-2 rounded-lg border text-[11px] ${
                      n.type === 'alert'
                        ? 'bg-rose-950/40 border-rose-500/30 text-rose-200'
                        : 'bg-slate-800/40 border-white/5 text-slate-300'
                    }`}
                  >
                    <div className="flex justify-between text-[10px] text-slate-400 mb-1">
                      <span>{n.time}</span>
                      <span className="font-bold">{n.type.toUpperCase()}</span>
                    </div>
                    <div>{n.message}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <button
          onClick={handleQuickPrediction}
          disabled={isLoading}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white text-xs font-semibold shadow-md shadow-emerald-950/50 transition-all cursor-pointer"
        >
          <Cpu className="w-3.5 h-3.5" />
          <span>{isLoading ? 'Running ML...' : 'Run AI Prediction'}</span>
        </button>

        <div className="relative">
          <button
            onClick={() => setShowResetConfirm(true)}
            disabled={isLoading}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700/80 disabled:opacity-50 text-slate-300 text-xs font-medium border border-white/10 transition-all cursor-pointer"
            title="Reset Simulation State"
          >
            <RotateCcw className="w-3.5 h-3.5 text-slate-400" />
            <span className="hidden md:inline">Reset Simulation</span>
          </button>

          {showResetConfirm && (
            <div className="absolute right-0 mt-2 w-64 bg-slate-900 border border-white/10 rounded-xl shadow-2xl p-3 z-50 text-xs">
              <p className="font-semibold text-white mb-1">Reset Simulation?</p>
              <p className="text-slate-400 text-[11px] mb-3">
                This will reset active sector readings and clear local SQLite telemetry for a clean demo run.
              </p>
              <div className="flex gap-2 justify-end">
                <button
                  onClick={() => setShowResetConfirm(false)}
                  className="px-2.5 py-1 rounded bg-slate-800 text-slate-300 text-[11px]"
                >
                  Cancel
                </button>
                <button
                  onClick={async () => {
                    setShowResetConfirm(false);
                    await resetFarm();
                  }}
                  className="px-2.5 py-1 rounded bg-rose-600 hover:bg-rose-500 text-white font-semibold text-[11px]"
                >
                  Confirm Reset
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
