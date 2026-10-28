import type {
  HealthResponse,
  ModelInfo,
  MetricsResponse,
  SensorPayload,
  PredictionResult,
  TelemetryRecord,
  AzureStatus,
} from '../types/api';

const API_BASE = '/api';

export const api = {
  async getHealth(): Promise<HealthResponse> {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error('Failed to reach backend health endpoint');
    return res.json();
  },

  async getModelInfo(): Promise<ModelInfo> {
    const res = await fetch(`${API_BASE}/model-info`);
    if (!res.ok) throw new Error('Failed to fetch model info');
    return res.json();
  },

  async getMetrics(): Promise<MetricsResponse> {
    const res = await fetch(`${API_BASE}/metrics`);
    if (!res.ok) throw new Error('Failed to fetch evaluation metrics');
    return res.json();
  },

  async predict(reading: SensorPayload): Promise<PredictionResult> {
    const res = await fetch(`${API_BASE}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(reading),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Prediction request failed' }));
      throw new Error(err.detail || 'Prediction failed');
    }
    return res.json();
  },

  async simulate(scenario?: string, count: number = 1): Promise<{ count: number; results: PredictionResult[] }> {
    const res = await fetch(`${API_BASE}/simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario: scenario || null, count }),
    });
    if (!res.ok) throw new Error('Simulation failed');
    return res.json();
  },

  async getTelemetry(limit: number = 100): Promise<{ total: number; records: TelemetryRecord[] }> {
    const res = await fetch(`${API_BASE}/telemetry?limit=${limit}`);
    if (!res.ok) throw new Error('Failed to fetch telemetry records');
    return res.json();
  },

  async getAzureStatus(): Promise<AzureStatus> {
    const res = await fetch(`${API_BASE}/azure-status`);
    if (!res.ok) throw new Error('Failed to fetch Azure status');
    return res.json();
  },

  async registerAzureModel(): Promise<any> {
    const res = await fetch(`${API_BASE}/azure-register`, { method: 'POST' });
    return res.json();
  },

  async resetSimulation(): Promise<{ message: string; baseline_created: boolean }> {
    const res = await fetch(`${API_BASE}/reset-simulation`, { method: 'POST' });
    if (!res.ok) throw new Error('Reset failed');
    return res.json();
  },

  getExportUrl(): string {
    return `${API_BASE}/export`;
  }
};
