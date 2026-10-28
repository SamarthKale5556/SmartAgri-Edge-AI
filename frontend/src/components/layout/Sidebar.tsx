import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  Sprout,
  Activity,
  Cpu,
  BarChart3,
  History,
  Cloud,
  FileText,
  AlertTriangle,
} from 'lucide-react';
import { useFarm } from '../../context/FarmContext';

export const Sidebar: React.FC = () => {
  const { health } = useFarm();
  const isModelActive = health?.edge_model_active ?? false;

  const navItems = [
    { to: '/', label: 'Farm Overview', icon: Sprout },
    { to: '/simulation', label: 'Live Farm Simulation', icon: Activity },
    { to: '/predictions', label: 'AI Predictions', icon: Cpu },
    { to: '/evaluation', label: 'Model Evaluation', icon: BarChart3 },
    { to: '/history', label: 'Telemetry History', icon: History },
    { to: '/azure', label: 'Azure ML & Edge', icon: Cloud },
    { to: '/project-info', label: 'Project Information', icon: FileText },
  ];

  return (
    <aside className="w-64 bg-[#0d1422] border-r border-white/10 flex flex-col justify-between shrink-0 h-screen sticky top-0 select-none">
      {/* Brand & Header */}
      <div>
        <div className="p-4 border-b border-white/10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-700 flex items-center justify-center shadow-lg shadow-emerald-900/30 border border-emerald-400/30">
              <Sprout className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-sm font-bold text-white tracking-tight flex items-center gap-1.5">
                AgriSense Edge AI
              </h1>
              <p className="text-[11px] font-medium text-emerald-400/90 tracking-wide">
                Samarth Kale's Workspace
              </p>
            </div>
          </div>

          {/* Genuine Edge Model Status Badge */}
          <div className="mt-3.5">
            {isModelActive ? (
              <div className="flex items-center gap-2 px-2.5 py-1.5 rounded-lg bg-emerald-950/80 border border-emerald-500/30 text-emerald-300 text-[11px] font-semibold">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                <span className="tracking-wide">EDGE MODEL ACTIVE</span>
              </div>
            ) : (
              <div className="flex items-center gap-2 px-2.5 py-1.5 rounded-lg bg-amber-950/80 border border-amber-500/30 text-amber-300 text-[11px] font-semibold">
                <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
                <span>MODEL OFFLINE</span>
              </div>
            )}
          </div>
        </div>

        {/* Navigation Menu */}
        <nav className="p-3 space-y-1">
          <div className="px-3 py-1.5 text-[10px] font-bold text-slate-400 uppercase tracking-wider">
            Navigation
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-gradient-to-r from-emerald-600 to-teal-700 text-white shadow-md shadow-emerald-950/50 font-semibold'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`
                }
              >
                <Icon className="w-4 h-4 shrink-0" />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* Footer / System Status & Student Profile */}
      <div className="p-3 border-t border-white/10 space-y-2.5 bg-[#0a0f18]/60">
        <div className="px-2.5 py-2 rounded-lg bg-slate-900/80 border border-white/5 text-[11px] space-y-1">
          <div className="flex items-center justify-between text-slate-400">
            <span>Model Artifact:</span>
            <span className="text-slate-200 font-mono text-[10px]">irrigation_model.joblib</span>
          </div>
          <div className="flex items-center justify-between text-slate-400">
            <span>Inference Runtime:</span>
            <span className="text-emerald-400 font-medium">Local Python Edge</span>
          </div>
          <div className="flex items-center justify-between text-slate-400">
            <span>Database:</span>
            <span className="text-slate-200 font-mono text-[10px]">SQLite (Connected)</span>
          </div>
        </div>

        <div className="flex items-center gap-2.5 px-2 py-1.5 rounded-lg bg-emerald-950/40 border border-emerald-500/20">
          <div className="w-7 h-7 rounded-full bg-emerald-800 flex items-center justify-center text-emerald-200 font-bold text-xs">
            SK
          </div>
          <div className="truncate">
            <span className="text-xs font-semibold text-white block truncate">Samarth Kale</span>
            <span className="text-[10px] text-emerald-400/80 block">Lead ML / Edge Engineer</span>
          </div>
        </div>
      </div>
    </aside>
  );
};
