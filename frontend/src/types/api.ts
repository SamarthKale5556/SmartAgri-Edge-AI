export interface HealthResponse {
  status: string;
  system: string;
  workspace: string;
  edge_model_loaded: boolean;
  edge_model_active: boolean;
  engine_load_time_ms: number;
  db_connected: boolean;
  timestamp: string;
}

export interface FeatureMetadata {
  name: string;
  type: string;
  unit: string;
  acceptable_range: [number, number];
}

export interface ModelInfo {
  model_name: string;
  version: string;
  framework: string;
  pipeline_stages: string[];
  artifact_path: string;
  file_size_bytes: number;
  last_modified: string;
  input_features: FeatureMetadata[];
  output_classes: Record<string | number, string>;
}

export interface ConfusionMatrix {
  tn: number;
  fp: number;
  fn: number;
  tp: number;
  matrix: number[][];
}

export interface EvaluationMetrics {
  model_name: string;
  model_version: string;
  framework: string;
  pipeline_stages: string[];
  dataset_size_total: number;
  train_samples: number;
  test_samples: number;
  features: string[];
  test_accuracy: number;
  test_precision: number;
  test_recall: number;
  test_f1_score: number;
  confusion_matrix: ConfusionMatrix;
  feature_importances: Record<string, number>;
  evaluation_notes: string;
}

export interface MetricsResponse {
  metrics: EvaluationMetrics;
  assumptions: any;
  is_synthetic: boolean;
  disclaimer: string;
}

export interface SensorPayload {
  soil_moisture_percent: number;
  temperature_c: number;
  humidity_percent: number;
  rainfall_mm: number;
  field_zone?: string;
}

export interface PredictionResult {
  success: boolean;
  timestamp: string;
  reading: SensorPayload;
  prediction: number;
  recommendation: string;
  action_code: 'VALVE_OPEN' | 'VALVE_CLOSED';
  confidence_score: number;
  irrigation_probability: number;
  latency_ms: number;
  status: string;
  error?: string;
}

export interface TelemetryRecord {
  id: number;
  timestamp: string;
  soil_moisture: number;
  temperature: number;
  humidity: number;
  rainfall: number;
  prediction: number;
  recommendation: string;
  action_code: string;
  confidence_score: number;
  irrigation_probability: number;
  latency_ms: number;
  status: string;
}

export interface AzureStatus {
  is_configured: boolean;
  subscription_id: string;
  resource_group: string;
  workspace_name: string;
  model_file_exists: boolean;
  model_path: string;
  last_receipt?: {
    success: boolean;
    status: string;
    timestamp: string;
    missing_parameters?: string[];
    message?: string;
    model_name?: string;
    model_version?: string;
  };
}
