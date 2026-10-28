import React, { useState } from 'react';
import { useFarm } from '../context/FarmContext';
import { api } from '../services/api';
import {
  Cpu,
  Download,
  Filter,
  CheckCircle2,
  AlertOctagon,
  Search,
} from 'lucide-react';

export const PredictionsPage: React.FC = () => {
  const { telemetry } = useFarm();
  const [filterClass, setFilterClass] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState<string>('');

  const filtered = telemetry.filter((rec) => {
    if (filterClass !== 'all') {
      const targetPred = filterClass === 'irrigate' ? 1 : 0;
      if (rec.prediction !== targetPred) return false;
    }
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      return (
        rec.timestamp.toLowerCase().includes(term) ||
        rec.action_code.toLowerCase().includes(term) ||
        rec.recommendation.toLowerCase().includes(term)
      );
    }
    return true;
  });

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-5 rounded-xl bg-slate-900/80 border border-white/10 shadow-xl">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Cpu className="w-5 h-5 text-emerald-400" />
            AI Prediction Analysis & Actuator Decisions
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Real-time inference records generated in-situ by the edge scikit-learn pipeline and persisted to SQLite.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <a
            href={api.getExportUrl()}
            download
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold shadow-md transition-all cursor-pointer"
          >
            <Download className="w-4 h-4" />
            <span>Download CSV Log</span>
          </a>
        </div>
      </div>

      <div className="p-4 rounded-xl bg-slate-900/80 border border-white/10 shadow-lg flex flex-col sm:flex-row gap-3 items-center justify-between">
        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search timestamp, action, notes..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 rounded-lg bg-slate-800 text-xs text-white placeholder-slate-400 border border-white/5 focus:outline-none focus:border-emerald-500"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Filter className="w-3.5 h-3.5 text-slate-400" />
          <span className="text-xs text-slate-400">Class Filter:</span>
          <select
            value={filterClass}
            onChange={(e) => setFilterClass(e.target.value)}
            className="px-3 py-1.5 rounded-lg bg-slate-800 text-xs text-slate-200 border border-white/5 focus:outline-none focus:border-emerald-500"
          >
            <option value="all">All Events ({telemetry.length})</option>
            <option value="irrigate">Irrigation Required (VALVE_OPEN)</option>
            <option value="conserve">Moisture Adequate (VALVE_CLOSED)</option>
          </select>
        </div>
      </div>

      <div className="rounded-xl bg-slate-900/80 border border-white/10 shadow-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950/80 text-[11px] font-bold text-slate-400 uppercase tracking-wider border-b border-white/10">
              <tr>
                <th className="py-3 px-4"># ID</th>
                <th className="py-3 px-4">Timestamp</th>
                <th className="py-3 px-4">Soil Moisture</th>
                <th className="py-3 px-4">Temp</th>
                <th className="py-3 px-4">Humidity</th>
                <th className="py-3 px-4">Rainfall</th>
                <th className="py-3 px-4">Prediction</th>
                <th className="py-3 px-4">Actuator Directive</th>
                <th className="py-3 px-4">Probability</th>
                <th className="py-3 px-4">Latency</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 text-slate-300">
              {filtered.length === 0 ? (
                <tr>
                  <td colSpan={10} className="py-8 text-center text-slate-500">
                    No prediction records match the criteria.
                  </td>
                </tr>
              ) : (
                filtered.map((row) => (
                  <tr key={row.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3 px-4 font-mono text-slate-500">#{row.id}</td>
                    <td className="py-3 px-4 font-mono text-slate-400 whitespace-nowrap">
                      {row.timestamp}
                    </td>
                    <td className="py-3 px-4 font-bold text-white">
                      <span
                        className={
                          row.soil_moisture < 20
                            ? 'text-rose-400'
                            : row.soil_moisture > 40
                            ? 'text-sky-400'
                            : 'text-emerald-400'
                        }
                      >
                        {row.soil_moisture}%
                      </span>
                    </td>
                    <td className="py-3 px-4 text-amber-300">{row.temperature}°C</td>
                    <td className="py-3 px-4 text-sky-300">{row.humidity}%</td>
                    <td className="py-3 px-4 text-blue-300">{row.rainfall} mm</td>
                    <td className="py-3 px-4 font-semibold">
                      {row.prediction === 1 ? (
                        <span className="text-rose-400">Irrigate (1)</span>
                      ) : (
                        <span className="text-emerald-400">Adequate (0)</span>
                      )}
                    </td>
                    <td className="py-3 px-4">
                      <span
                        className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                          row.action_code === 'VALVE_OPEN'
                            ? 'bg-rose-950 text-rose-300 border border-rose-800'
                            : 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                        }`}
                      >
                        {row.action_code === 'VALVE_OPEN' ? (
                          <AlertOctagon className="w-3 h-3 text-rose-400" />
                        ) : (
                          <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                        )}
                        {row.action_code}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-mono text-amber-400 font-semibold">
                      {(row.irrigation_probability * 100).toFixed(1)}%
                    </td>
                    <td className="py-3 px-4 font-mono text-slate-400">
                      {row.latency_ms.toFixed(1)} ms
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      <div className="p-4 rounded-xl bg-slate-900/60 border border-amber-500/20 text-xs text-amber-200/80">
        ⚠️ <strong>Epistemic Honesty Notice:</strong> Predictions represent statistical vote majorities across 100 decision trees trained on synthetic agro-heuristic rules. They do not constitute measured physical matric water potential in soil.
      </div>
    </div>
  );
};
