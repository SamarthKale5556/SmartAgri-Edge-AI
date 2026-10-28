import React from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { FarmProvider } from './context/FarmContext';
import { Sidebar } from './components/layout/Sidebar';
import { TopBar } from './components/layout/TopBar';

import { FarmOverviewPage } from './pages/FarmOverviewPage';
import { LiveSimulationPage } from './pages/LiveSimulationPage';
import { PredictionsPage } from './pages/PredictionsPage';
import { EvaluationPage } from './pages/EvaluationPage';
import { TelemetryHistoryPage } from './pages/TelemetryHistoryPage';
import { AzureEdgePage } from './pages/AzureEdgePage';
import { ProjectInfoPage } from './pages/ProjectInfoPage';

const AppContent: React.FC = () => {
  const location = useLocation();

  const getPageMeta = (pathname: string) => {
    switch (pathname) {
      case '/':
        return {
          title: 'Farm Command Centre & 3D Digital Twin',
          desc: 'Real-time multi-sector telemetry, interactive 3D field model, and in-situ ML predictions.',
        };
      case '/simulation':
        return {
          title: 'Live IoT Telemetry Simulator',
          desc: 'Generate stochastic readings, inject agro-scenarios, and test edge actuator response.',
        };
      case '/predictions':
        return {
          title: 'AI Prediction Log & Actuator Directives',
          desc: 'Historical inference decisions emitted by the local scikit-learn edge pipeline.',
        };
      case '/evaluation':
        return {
          title: 'Model Evaluation & Verification',
          desc: 'Held-out test split performance (88.20% accuracy), confusion matrix, and feature importances.',
        };
      case '/history':
        return {
          title: 'Telemetry History & Sensor Dynamics',
          desc: 'Searchable SQLite event records, time-series trends, and CSV audit download.',
        };
      case '/azure':
        return {
          title: 'Azure ML MLOps & IoT Edge Architecture',
          desc: 'Edge-first execution model with optional Azure ML SDK v2 versioned model registry.',
        };
      case '/project-info':
        return {
          title: 'PBA-2 Project Specification & Architecture',
          desc: 'Domain problem statement, system data flow, and student author details.',
        };
      default:
        return {
          title: 'AgriSense Edge AI',
          desc: 'Smart Agriculture IoT Edge System',
        };
    }
  };

  const meta = getPageMeta(location.pathname);

  return (
    <div className="flex min-h-screen bg-[#0a0f18] text-slate-100">
      {/* Fixed Left Navigation Sidebar */}
      <Sidebar />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-y-auto">
        <TopBar title={meta.title} description={meta.desc} />
        <main className="flex-1 pb-12">
          <Routes>
            <Route path="/" element={<FarmOverviewPage />} />
            <Route path="/simulation" element={<LiveSimulationPage />} />
            <Route path="/predictions" element={<PredictionsPage />} />
            <Route path="/evaluation" element={<EvaluationPage />} />
            <Route path="/history" element={<TelemetryHistoryPage />} />
            <Route path="/azure" element={<AzureEdgePage />} />
            <Route path="/project-info" element={<ProjectInfoPage />} />
            <Route path="*" element={<FarmOverviewPage />} />
          </Routes>
        </main>
      </div>
    </div>
  );
};

export default function App() {
  return (
    <BrowserRouter>
      <FarmProvider>
        <AppContent />
      </FarmProvider>
    </BrowserRouter>
  );
}
