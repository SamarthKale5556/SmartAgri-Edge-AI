import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { api } from '../services/api';
import type { HealthResponse, PredictionResult, TelemetryRecord, SensorPayload } from '../types/api';

export interface FieldZoneInfo {
  id: string;
  name: string;
  cropType: string;
  growthStage: string;
  soilMoisture: number;
  temperature: number;
  humidity: number;
  rainfall: number;
  status: 'OPTIMAL' | 'DEFICIT' | 'IRRIGATING' | 'SATURATED';
  irrigationProbability: number;
}

interface FarmContextType {
  health: HealthResponse | null;
  latestPrediction: PredictionResult | null;
  telemetry: TelemetryRecord[];
  activeZoneId: string;
  fieldZones: Record<string, FieldZoneInfo>;
  isIrrigating: boolean;
  isLoading: boolean;
  error: string | null;
  simulatedWeather: {
    condition: string;
    temp: number;
    humidity: number;
    evaporationRisk: 'Low' | 'Moderate' | 'High' | 'Severe';
  };
  notifications: Array<{ id: string; time: string; message: string; type: 'info' | 'warning' | 'alert' }>;
  setActiveZoneId: (id: string) => void;
  runPrediction: (payload: SensorPayload) => Promise<PredictionResult>;
  runSimulation: (scenario?: string, count?: number) => Promise<void>;
  resetFarm: () => Promise<void>;
  refreshTelemetry: () => Promise<void>;
}

const DEFAULT_ZONES: Record<string, FieldZoneInfo> = {
  'North-Field-A': {
    id: 'North-Field-A',
    name: 'Sector 1 (Wheat / Vegetative)',
    cropType: 'Winter Wheat',
    growthStage: 'Tillering (Day 42)',
    soilMoisture: 22.4,
    temperature: 31.5,
    humidity: 42.0,
    rainfall: 0.0,
    status: 'DEFICIT',
    irrigationProbability: 0.88,
  },
  'North-Field-B': {
    id: 'North-Field-B',
    name: 'Sector 2 (Corn / Emergence)',
    cropType: 'Field Corn',
    growthStage: 'V3 Stage (Day 25)',
    soilMoisture: 38.2,
    temperature: 28.0,
    humidity: 58.0,
    rainfall: 1.2,
    status: 'OPTIMAL',
    irrigationProbability: 0.18,
  },
  'South-Field-A': {
    id: 'South-Field-A',
    name: 'Sector 3 (Soybean / Podding)',
    cropType: 'Soybeans',
    growthStage: 'R3 Pod Development (Day 65)',
    soilMoisture: 18.5,
    temperature: 35.2,
    humidity: 32.0,
    rainfall: 0.0,
    status: 'DEFICIT',
    irrigationProbability: 0.94,
  },
  'South-Field-B': {
    id: 'South-Field-B',
    name: 'Sector 4 (Barley / Ripe)',
    cropType: 'Barley',
    growthStage: 'Dough Stage (Day 80)',
    soilMoisture: 44.0,
    temperature: 24.0,
    humidity: 72.0,
    rainfall: 14.0,
    status: 'SATURATED',
    irrigationProbability: 0.04,
  },
};

const FarmContext = createContext<FarmContextType | undefined>(undefined);

export const FarmProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [latestPrediction, setLatestPrediction] = useState<PredictionResult | null>(null);
  const [telemetry, setTelemetry] = useState<TelemetryRecord[]>([]);
  const [activeZoneId, setActiveZoneId] = useState<string>('North-Field-A');
  const [fieldZones, setFieldZones] = useState<Record<string, FieldZoneInfo>>(DEFAULT_ZONES);
  const [isIrrigating, setIsIrrigating] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [notifications, setNotifications] = useState<Array<{ id: string; time: string; message: string; type: 'info' | 'warning' | 'alert' }>>([
    {
      id: 'init-1',
      time: new Date().toLocaleTimeString(),
      message: 'AgriSense Edge AI runtime initialized successfully on Windows local host.',
      type: 'info'
    }
  ]);

  const simulatedWeather = {
    condition: 'Sunny • Diurnal Radiation Peak',
    temp: latestPrediction?.reading.temperature_c ?? 31.5,
    humidity: latestPrediction?.reading.humidity_percent ?? 42.0,
    evaporationRisk: ((latestPrediction?.reading.temperature_c ?? 31.5) > 33 ? 'Severe' : 'Moderate') as 'Severe' | 'Moderate'
  };

  const refreshTelemetry = useCallback(async () => {
    try {
      const data = await api.getTelemetry(80);
      setTelemetry(data.records);
      if (data.records.length > 0) {
        const top = data.records[0];
        setIsIrrigating(top.action_code === 'VALVE_OPEN');
      }
    } catch (e: any) {
      console.warn('Could not fetch telemetry:', e.message);
    }
  }, []);

  useEffect(() => {
    api.getHealth()
      .then(setHealth)
      .catch((e) => setError(`Backend unreachable: ${e.message}`));
    refreshTelemetry();
  }, [refreshTelemetry]);

  const runPrediction = async (payload: SensorPayload): Promise<PredictionResult> => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await api.predict(payload);
      setLatestPrediction(result);
      const valveOpen = result.action_code === 'VALVE_OPEN';
      setIsIrrigating(valveOpen);

      const zoneKey = payload.field_zone || activeZoneId;
      setFieldZones((prev) => ({
        ...prev,
        [zoneKey]: {
          ...prev[zoneKey],
          soilMoisture: payload.soil_moisture_percent,
          temperature: payload.temperature_c,
          humidity: payload.humidity_percent,
          rainfall: payload.rainfall_mm,
          status: valveOpen ? 'IRRIGATING' : payload.soil_moisture_percent > 42 ? 'SATURATED' : 'OPTIMAL',
          irrigationProbability: result.irrigation_probability,
        }
      }));

      const notifType = valveOpen ? 'alert' : 'info';
      const notifMsg = valveOpen
        ? `🚨 IRRIGATION TRIGGERED in ${zoneKey} (Moisture: ${payload.soil_moisture_percent}%, Prob: ${(result.irrigation_probability * 100).toFixed(1)}%)`
        : `✅ Moisture adequate in ${zoneKey} (${payload.soil_moisture_percent}%). Valve kept closed.`;
      
      setNotifications((prev) => [
        { id: Date.now().toString(), time: new Date().toLocaleTimeString(), message: notifMsg, type: notifType },
        ...prev.slice(0, 15)
      ]);

      await refreshTelemetry();
      return result;
    } catch (e: any) {
      setError(e.message);
      throw e;
    } finally {
      setIsLoading(false);
    }
  };

  const runSimulation = async (scenario?: string, count: number = 1) => {
    setIsLoading(true);
    setError(null);
    try {
      const simRes = await api.simulate(scenario, count);
      if (simRes.results && simRes.results.length > 0) {
        const last = simRes.results[simRes.results.length - 1];
        setLatestPrediction(last);
        setIsIrrigating(last.action_code === 'VALVE_OPEN');
        
        setNotifications((prev) => [
          {
            id: Date.now().toString(),
            time: new Date().toLocaleTimeString(),
            message: `Simulated ${count} telemetry packets [${scenario || 'Stochastic'}]. Latency: ${last.latency_ms} ms.`,
            type: 'info'
          },
          ...prev.slice(0, 15)
        ]);
      }
      await refreshTelemetry();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setIsLoading(false);
    }
  };

  const resetFarm = async () => {
    setIsLoading(true);
    try {
      await api.resetSimulation();
      setFieldZones(DEFAULT_ZONES);
      setIsIrrigating(false);
      setLatestPrediction(null);
      setNotifications([
        {
          id: Date.now().toString(),
          time: new Date().toLocaleTimeString(),
          message: 'Simulation state & edge telemetry reset to baseline.',
          type: 'info'
        }
      ]);
      await refreshTelemetry();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <FarmContext.Provider
      value={{
        health,
        latestPrediction,
        telemetry,
        activeZoneId,
        fieldZones,
        isIrrigating,
        isLoading,
        error,
        simulatedWeather,
        notifications,
        setActiveZoneId,
        runPrediction,
        runSimulation,
        resetFarm,
        refreshTelemetry,
      }}
    >
      {children}
    </FarmContext.Provider>
  );
};

export const useFarm = () => {
  const context = useContext(FarmContext);
  if (!context) throw new Error('useFarm must be used within FarmProvider');
  return context;
};
