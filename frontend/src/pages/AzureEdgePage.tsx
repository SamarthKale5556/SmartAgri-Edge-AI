import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { AzureStatus } from '../types/api';
import {
  Cloud,
  Cpu,
  Server,
  CheckCircle2,
  AlertTriangle,
  Play,
  Terminal,
} from 'lucide-react';

export const AzureEdgePage: React.FC = () => {
  const [azureStatus, setAzureStatus] = useState<AzureStatus | null>(null);
  const [regResult, setRegResult] = useState<any | null>(null);
  const [isRegistering, setIsRegistering] = useState<boolean>(false);

  useEffect(() => {
    api.getAzureStatus()
      .then((res) => setAzureStatus(res))
      .catch(() => {});
  }, []);

  const handleRegister = async () => {
    setIsRegistering(true);
    setRegResult(null);
    try {
      const res = await api.registerAzureModel();
      setRegResult(res);
      const updated = await api.getAzureStatus();
      setAzureStatus(updated);
    } catch (e: any) {
      setRegResult({ success: false, error: e.message });
    } finally {
      setIsRegistering(false);
    }
  };

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Cloud className="w-5 h-5 text-indigo-400" />
            Azure Machine Learning Lifecycle & IoT Edge Runtime
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Edge-first execution model with optional enterprise MLOps model registry integration via Azure ML SDK v2.
          </p>
        </div>

        <button
          onClick={handleRegister}
          disabled={isRegistering}
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-xs font-semibold shadow-lg transition-all cursor-pointer"
        >
          <Play className="w-3.5 h-3.5" />
          <span>{isRegistering ? 'Registering with Azure ML...' : 'Attempt Azure ML Registration'}</span>
        </button>
      </div>

      {regResult && (
        <div
          className={`p-4 rounded-xl border text-xs ${
            regResult.success
              ? 'bg-emerald-950/70 border-emerald-500/40 text-emerald-200'
              : 'bg-amber-950/70 border-amber-500/40 text-amber-200'
          }`}
        >
          <div className="flex items-center gap-2 font-bold mb-1">
            {regResult.success ? (
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            ) : (
              <AlertTriangle className="w-4 h-4 text-amber-400" />
            )}
            <span>Status: {regResult.status}</span>
          </div>
          <p className="text-[11px] mt-1 leading-relaxed">
            {regResult.message || regResult.error || 'Registration response received.'}
          </p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="p-5 rounded-xl bg-slate-900/80 border border-emerald-500/30 shadow-xl space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-white/10">
            <div className="flex items-center gap-2">
              <Cpu className="w-5 h-5 text-emerald-400" />
              <h4 className="text-xs font-bold text-white uppercase tracking-wider">
                Autonomous Local Edge Runtime
              </h4>
            </div>
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-950 text-emerald-300 border border-emerald-700">
              CURRENTLY ACTIVE
            </span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="flex justify-between py-1.5 border-b border-white/5">
              <span className="text-slate-400">Execution Plane:</span>
              <span className="font-semibold text-white">Local In-Situ Python / CPython</span>
            </div>
            <div className="flex justify-between py-1.5 border-b border-white/5">
              <span className="text-slate-400">Model Artifact:</span>
              <span className="font-mono text-emerald-400">models/irrigation_model.joblib</span>
            </div>
            <div className="flex justify-between py-1.5 border-b border-white/5">
              <span className="text-slate-400">Telemetry Storage:</span>
              <span className="font-mono text-white">SQLite (data/edge_telemetry.db)</span>
            </div>
            <div className="flex justify-between py-1.5 border-b border-white/5">
              <span className="text-slate-400">Inference Latency:</span>
              <span className="font-mono text-emerald-400">&lt; 75 ms</span>
            </div>
            <div className="flex justify-between py-1.5">
              <span className="text-slate-400">Offline Resilience:</span>
              <span className="font-semibold text-emerald-300">100% (Zero Cloud Dependency)</span>
            </div>
          </div>

          <div className="p-3 rounded-lg bg-emerald-950/30 border border-emerald-500/20 text-[11px] text-emerald-200/90 leading-relaxed">
            The local edge engine loads the trained Random Forest model directly into memory once. Readings are validated and scored on the field node without transmitting sensitive agro-telemetry over internet networks.
          </div>
        </div>

        <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 shadow-xl space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-white/10">
            <div className="flex items-center gap-2">
              <Server className="w-5 h-5 text-indigo-400" />
              <h4 className="text-xs font-bold text-white uppercase tracking-wider">
                Azure Machine Learning Control Plane
              </h4>
            </div>
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-slate-800 text-slate-300 border border-white/10">
              OPTIONAL / MLOPS
            </span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="flex justify-between py-1.5 border-b border-white/5">
              <span className="text-slate-400">Subscription ID:</span>
              <span className="font-mono text-slate-300">{azureStatus?.subscription_id ?? 'Not Set'}</span>
            </div>
            <div className="flex justify-between py-1.5 border-b border-white/5">
              <span className="text-slate-400">Resource Group:</span>
              <span className="font-mono text-slate-300">{azureStatus?.resource_group ?? 'Not Set'}</span>
            </div>
            <div className="flex justify-between py-1.5 border-b border-white/5">
              <span className="text-slate-400">Workspace Name:</span>
              <span className="font-mono text-slate-300">{azureStatus?.workspace_name ?? 'Not Set'}</span>
            </div>
            <div className="flex justify-between py-1.5 border-b border-white/5">
              <span className="text-slate-400">SDK Version:</span>
              <span className="font-mono text-indigo-400">Azure ML SDK v2 (azure.ai.ml)</span>
            </div>
            <div className="flex justify-between py-1.5">
              <span className="text-slate-400">Cloud Status:</span>
              <span className="font-semibold text-amber-300">Standby (No Cloud Locked Token)</span>
            </div>
          </div>

          <div className="p-3 rounded-lg bg-slate-800/60 border border-white/5 text-[11px] text-slate-400 leading-relaxed">
            Azure ML functions as an asynchronous MLOps plane for seasonal retraining and model asset versioning. It is decoupled from the live second-by-second valve control loop.
          </div>
        </div>
      </div>

      <div className="p-5 rounded-xl bg-slate-900/80 border border-white/10 shadow-xl space-y-3">
        <div className="flex items-center gap-2 pb-2 border-b border-white/10">
          <Terminal className="w-4 h-4 text-emerald-400" />
          <h4 className="text-xs font-bold text-white uppercase tracking-wider">
            How to Authenticate & Register in Azure ML (PowerShell)
          </h4>
        </div>

        <pre className="p-4 rounded-lg bg-slate-950 border border-white/10 text-xs font-mono text-emerald-300 overflow-x-auto leading-relaxed">
{`# 1. Log in to your Azure subscription
az login

# 2. Configure target Azure ML Workspace environment variables
$env:AZURE_SUBSCRIPTION_ID="your-subscription-uuid"
$env:AZURE_RESOURCE_GROUP="rg-smart-agriculture"
$env:AZURE_WORKSPACE_NAME="mlw-smartagri-edge"

# 3. Execute model asset registration
python register_azure_model.py`}
        </pre>
      </div>
    </div>
  );
};
