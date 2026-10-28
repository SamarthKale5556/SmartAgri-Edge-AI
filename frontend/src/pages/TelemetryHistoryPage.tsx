import React, { useState } from 'react';
import { useFarm } from '../context/FarmContext';
import { api } from '../services/api';
import {
  History,
  Download,
  Search,
  Filter,
  TrendingUp,
  AlertOctagon,
  CheckCircle2,
} from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
  ReferenceLine,
} from 'recharts';

export const TelemetryHistoryPage: React.FC = () => {
  const { telemetry } = useFarm();
  const [filterAction, setFilterAction] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState<string>('');

  const chartData = [...telemetry].reverse().map((t, idx) => ({
    id: t.id,
    time: t.timestamp.split(' ')[1] || `T${idx}`,
    soilMoisture: t.soil_moisture,
    temperature: t.temperature,
    humidity: t.humidity,
    action: t.action_code,
  }));

  const filtered = telemetry.filter((t) => {
    if (filterAction !== 'all' && t.action_code !== filterAction) return false;
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      return (
        t.timestamp.toLowerCase().includes(term) ||
        t.recommendation.toLowerCase().includes(term) ||
        t.action_code.toLowerCase().includes(term)
      );
    }
    return true;
  });

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 shadow-xl flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <History className="w-5 h-5 text-emerald-400" />
            Edge Telemetry History & Time-Series Auditing
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Persisted in-situ records from local SQLite database (<code>edge_telemetry.db</code>).
          </p>
        </div>

        <a
          href={api.getExportUrl()}
          download
          className="flex items-center gap-2 px-3.5 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold shadow-md transition-all cursor-pointer"
        >
          <Download className="w-4 h-4" />
          <span>Export SQLite to CSV</span>
        </a>
      </div>

      <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 shadow-xl space-y-3">
        <div className="flex items-center justify-between pb-2 border-b border-white/10">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-emerald-400" />
            <h4 className="text-xs font-bold text-white uppercase tracking-wider">
              Environmental Sensor Dynamics vs. Critical Deficit Threshold
            </h4>
          </div>
          <span className="text-[11px] text-slate-400 font-mono">
            {chartData.length} Events Processed
          </span>
        </div>

        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <XAxis dataKey="time" stroke="#64748b" fontSize={11} />
              <YAxis stroke="#64748b" fontSize={11} domain={[0, 100]} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
              />
              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
              <ReferenceLine y={20} stroke="#f59e0b" strokeDasharray="4 4" label={{ value: 'Critical Deficit (20%)', fill: '#f59e0b', fontSize: 10 }} />
              <Line type="monotone" dataKey="soilMoisture" name="Soil Moisture (%)" stroke="#10b981" strokeWidth={2.5} dot={false} />
              <Line type="monotone" dataKey="temperature" name="Temp (°C)" stroke="#ef4444" strokeWidth={1.5} dot={false} />
              <Line type="monotone" dataKey="humidity" name="Humidity (%)" stroke="#3b82f6" strokeWidth={1.5} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="p-4 rounded-xl bg-slate-900/80 border border-white/10 shadow-lg flex flex-col sm:flex-row gap-3 items-center justify-between">
        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search records..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 rounded-lg bg-slate-800 text-xs text-white placeholder-slate-400 border border-white/5 focus:outline-none focus:border-emerald-500"
          />
        </div>

        <div className="flex items-center gap-2">
          <Filter className="w-3.5 h-3.5 text-slate-400" />
          <span className="text-xs text-slate-400">Action:</span>
          <select
            value={filterAction}
            onChange={(e) => setFilterAction(e.target.value)}
            className="px-3 py-1.5 rounded-lg bg-slate-800 text-xs text-slate-200 border border-white/5"
          >
            <option value="all">All Directives ({telemetry.length})</option>
            <option value="VALVE_OPEN">VALVE_OPEN (Irrigation Cycles)</option>
            <option value="VALVE_CLOSED">VALVE_CLOSED (Conserve)</option>
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
                <th className="py-3 px-4">Directive</th>
                <th className="py-3 px-4">Recommendation</th>
                <th className="py-3 px-4">Probability</th>
                <th className="py-3 px-4">Latency</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 text-slate-300">
              {filtered.length === 0 ? (
                <tr>
                  <td colSpan={10} className="py-8 text-center text-slate-500">
                    No telemetry records available in SQLite.
                  </td>
                </tr>
              ) : (
                filtered.map((row) => (
                  <tr key={row.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3 px-4 font-mono text-slate-500">#{row.id}</td>
                    <td className="py-3 px-4 font-mono text-slate-400 whitespace-nowrap">{row.timestamp}</td>
                    <td className="py-3 px-4 font-bold text-white">
                      <span className={row.soil_moisture < 20 ? 'text-rose-400' : 'text-emerald-400'}>
                        {row.soil_moisture}%
                      </span>
                    </td>
                    <td className="py-3 px-4 text-amber-300">{row.temperature}°C</td>
                    <td className="py-3 px-4 text-sky-300">{row.humidity}%</td>
                    <td className="py-3 px-4 text-blue-300">{row.rainfall} mm</td>
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
                    <td className="py-3 px-4 text-slate-300 max-w-xs truncate">{row.recommendation}</td>
                    <td className="py-3 px-4 font-mono text-amber-400 font-semibold">
                      {(row.irrigation_probability * 100).toFixed(1)}%
                    </td>
                    <td className="py-3 px-4 font-mono text-slate-400">{row.latency_ms.toFixed(1)} ms</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
