"""
generate_pdf_report.py - Publication-Grade Academic PDF Report Generator
Designed for Samarth Kale's Activity-1 PBA-2 Practical Examination Submission
"""

import os
import subprocess
import base64

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "docs", "screenshots")
HTML_OUTPUT = os.path.join(BASE_DIR, "report_temp.html")
PDF_OUTPUT = os.path.join(BASE_DIR, "SMART_IRRIGATION_ACTIVITY1_REPORT.pdf")

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe"
]

def img_to_b64(filename):
    path = os.path.join(SCREENSHOTS_DIR, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

img1 = img_to_b64("01_farm_3d_digital_twin.png")
img2 = img_to_b64("02_live_telemetry_simulator.png")
img3 = img_to_b64("03_field_sector_environment.png")
img4 = img_to_b64("04_telemetry_history_dynamics.png")
img5 = img_to_b64("05_model_evaluation_metrics.png")
img6 = img_to_b64("06_azure_ml_registered_model.png")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Activity-1 Smart Irrigation Edge AI Report - Samarth Kale</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 12mm 14mm 12mm 14mm;
  }}

  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}

  body {{
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background: #ffffff;
    line-height: 1.42;
    font-size: 9pt;
    margin: 0;
    padding: 0;
  }}

  /* Page Wrapper to guarantee precise pagination */
  .report-page {{
    page-break-after: always;
    min-height: 270mm;
    position: relative;
    padding-bottom: 24px;
  }}

  .report-page:last-child {{
    page-break-after: avoid;
  }}

  /* Running Page Footer */
  .page-footer {{
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    border-top: 1px solid #e2e8f0;
    padding-top: 4px;
    font-size: 7.5pt;
    color: #64748b;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .page-footer span.bold {{
    font-weight: 700;
    color: #0284c7;
  }}

  /* Top Academic Header Block */
  .institution-header {{
    border-bottom: 2px solid #0284c7;
    padding-bottom: 8px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .institution-header .inst-title {{
    font-size: 13pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.3px;
  }}

  .institution-header .inst-sub {{
    font-size: 8.5pt;
    color: #64748b;
    font-weight: 600;
  }}

  .institution-header .exam-badge {{
    background: #0284c7;
    color: #ffffff;
    padding: 5px 12px;
    border-radius: 5px;
    font-size: 8.5pt;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }}

  /* Cover Card */
  .title-card {{
    background: linear-gradient(135deg, #060B18 0%, #0F1A3A 100%);
    color: #ffffff;
    padding: 16px 20px;
    border-radius: 8px;
    margin-bottom: 14px;
    border-left: 5px solid #00F0FF;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  }}

  .title-card h1 {{
    margin: 0 0 4px 0;
    font-size: 15.5pt;
    font-weight: 800;
    color: #38bdf8;
    letter-spacing: -0.3px;
  }}

  .title-card h2 {{
    margin: 0 0 10px 0;
    font-size: 9.5pt;
    font-weight: 500;
    color: #cbd5e1;
  }}

  /* Credentials Grid */
  .cred-table {{
    width: 100%;
    border-collapse: collapse;
    background: rgba(255, 255, 255, 0.06);
    border-radius: 6px;
    overflow: hidden;
  }}

  .cred-table td {{
    padding: 5px 9px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    font-size: 8.5pt;
  }}

  .cred-table td.label {{
    color: #94a3b8;
    width: 22%;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 7.5pt;
  }}

  .cred-table td.val {{
    color: #ffffff;
    font-weight: 700;
  }}

  /* Headings */
  h2.sec-title {{
    font-size: 11pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 1.5px solid #e2e8f0;
    padding-bottom: 3px;
    margin-top: 12px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 7px;
  }}

  h2.sec-title span.num {{
    background: #0284c7;
    color: #ffffff;
    width: 20px;
    height: 20px;
    border-radius: 4px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 8pt;
  }}

  p, li {{
    color: #334155;
    font-size: 8.8pt;
    margin-bottom: 5px;
    text-align: justify;
  }}

  ul, ol {{
    margin-top: 3px;
    margin-bottom: 8px;
    padding-left: 18px;
  }}

  li {{
    margin-bottom: 3px;
  }}

  /* Tables */
  table.content-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0 10px 0;
    font-size: 8.5pt;
  }}

  table.content-table th {{
    background: #0f172a;
    color: #f8fafc;
    padding: 6px 9px;
    text-align: left;
    font-weight: 700;
    border: 1px solid #1e293b;
    font-size: 8pt;
  }}

  table.content-table td {{
    padding: 5px 9px;
    border: 1px solid #cbd5e1;
    color: #334155;
    vertical-align: middle;
  }}

  table.content-table tr:nth-child(even) {{
    background: #f8fafc;
  }}

  /* Metrics Summary Boxes */
  .metrics-row {{
    display: flex;
    gap: 8px;
    margin: 10px 0 12px 0;
  }}

  .metric-card {{
    flex: 1;
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px 6px;
    text-align: center;
  }}

  .metric-card.accent {{
    background: #f0fdf4;
    border-color: #22c55e;
  }}

  .metric-card .label {{
    font-size: 7pt;
    text-transform: uppercase;
    font-weight: 700;
    color: #64748b;
  }}

  .metric-card .value {{
    font-size: 13.5pt;
    font-weight: 800;
    color: #0f172a;
    font-family: 'Consolas', monospace;
    margin: 2px 0;
  }}

  .metric-card .sub {{
    font-size: 7pt;
    font-weight: 600;
    color: #16a34a;
  }}

  /* Screenshots */
  .shot-card {{
    margin: 10px 0;
    border: 1px solid #0284c7;
    border-radius: 6px;
    overflow: hidden;
    background: #060B18;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
  }}

  .shot-card img {{
    width: 100%;
    max-height: 255px;
    object-fit: contain;
    display: block;
    background: #060B18;
  }}

  .shot-caption {{
    background: #0f172a;
    color: #38bdf8;
    font-size: 8pt;
    padding: 5px 10px;
    font-weight: 600;
    border-top: 1px solid #1e293b;
    display: flex;
    justify-content: space-between;
  }}

  .shot-caption span.fig-id {{
    color: #facc15;
    font-weight: 700;
  }}

  .shot-desc {{
    background: #f8fafc;
    color: #475569;
    font-size: 7.8pt;
    padding: 4px 10px;
    border-top: 1px solid #e2e8f0;
    line-height: 1.35;
  }}

  /* Workflow Boxes */
  .flow-box {{
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-left: 3.5px solid #0284c7;
    border-radius: 5px;
    padding: 8px 12px;
    margin: 6px 0;
    font-size: 8.5pt;
  }}

  .flow-step {{
    display: flex;
    align-items: flex-start;
    gap: 7px;
    margin-bottom: 5px;
  }}

  .flow-step:last-child {{
    margin-bottom: 0;
  }}

  .flow-step .num {{
    background: #0284c7;
    color: white;
    font-weight: 700;
    font-size: 7.5pt;
    padding: 1px 5px;
    border-radius: 3px;
  }}

  code {{
    font-family: 'Consolas', monospace;
    background: #f1f5f9;
    color: #0369a1;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 8pt;
  }}
</style>
</head>
<body>

  <!-- ==================== PAGE 1: TITLE, CREDENTIALS, AIM & THEORY ==================== -->
  <div class="report-page">
    <div class="institution-header">
      <div>
        <div class="inst-title">Department of Artificial Intelligence & Data Science</div>
        <div class="inst-sub">Practical-Based Assessment (PBA-2) • Academic Examination Report</div>
      </div>
      <div class="exam-badge">Activity-1 Report</div>
    </div>

    <div class="title-card">
      <h1>🌾 SMART AGRICULTURE IRRIGATION SYSTEM AT THE IOT EDGE</h1>
      <h2>Autonomous Cyber-Physical Precision Agriculture via Edge AI & Azure Machine Learning</h2>
      
      <table class="cred-table">
        <tr>
          <td class="label">Candidate Name</td>
          <td class="val">SAMARTH KALE</td>
          <td class="label">Enrollment No.</td>
          <td class="val">ADT23SOCB0955</td>
        </tr>
        <tr>
          <td class="label">Division / Roll No.</td>
          <td class="val">AIEC02 / Roll No: 37</td>
          <td class="label">Course Module</td>
          <td class="val">PBA-2: Edge Machine Learning</td>
        </tr>
        <tr>
          <td class="label">Azure Workspace</td>
          <td class="val">ml-assignment5-samarthkale</td>
          <td class="label">Registered Model</td>
          <td class="val">smart-irrigation-edge-rf:1</td>
        </tr>
        <tr>
          <td class="label">GitHub Repository</td>
          <td class="val" colspan="3">https://github.com/SamarthKale5556/SmartAgri-Edge-AI</td>
        </tr>
      </table>
    </div>

    <!-- 1. AIM -->
    <h2 class="sec-title"><span class="num">1</span> Aim of the Project</h2>
    <p>
      To design, train, evaluate, and deploy an <strong>autonomous Edge Machine Learning system</strong> capable of predicting real-time agricultural crop irrigation needs (<code>VALVE_OPEN</code> vs <code>VALVE_CLOSED</code>) based on live environmental sensor telemetry (Soil Moisture, Canopy Temperature, Relative Humidity, and Precipitation), achieving <strong>sub-100 millisecond inference latency</strong> and 100% offline operational reliability, integrated with <strong>Azure Machine Learning Studio</strong> for centralized MLOps governance.
    </p>

    <!-- 2. THEORY -->
    <h2 class="sec-title"><span class="num">2</span> Theoretical Foundation & Agronomic Working Principle</h2>
    <p>
      Traditional farming employs timer-based or manual flooding schedules, generating two catastrophic agronomic failure modes:
    </p>
    <ul>
      <li><strong>Over-Irrigation:</strong> Induces root-zone hypoxia (root rot), leaches critical nitrogen and potassium nutrients into the regional water table, and wastes up to 35% of fresh water resources.</li>
      <li><strong>Under-Irrigation:</strong> Induces vegetative drought stress, triggers guard cell stomatal closure, suppresses chlorophyll synthesis, and causes irreversible crop yield reduction.</li>
      <li><strong>The Rural Connectivity Gap:</strong> Remote agricultural acreage frequently experiences intermittent or non-existent cellular internet. Cloud-only architectures fail during connectivity dropouts, leaving actuator valves frozen in undefined states.</li>
    </ul>
    <p>
      <strong>The Edge AI Solution:</strong> We deploy an optimized <strong>Random Forest Classifier</strong> pipeline directly onto an on-site edge gateway. The system receives real-time analog/digital sensor readings, normalizes input distributions via <code>StandardScaler</code>, predicts crop water deficit probability, and switches the physical solenoid relay valve completely offline.
    </p>

    <div class="flow-box">
      <strong>Mathematical Evapotranspiration Decision Rule:</strong><br>
      <code>Directive = VALVE_OPEN (1) &nbsp;IF&nbsp; P(Deficit | Moisture, Temp, Humidity, Rain) &ge; 0.50 &nbsp;ELSE&nbsp; VALVE_CLOSED (0)</code>
    </div>

    <div class="page-footer">
      <span>Activity-1: Smart Irrigation Edge AI • Practical-Based Assessment (PBA-2)</span>
      <span>Page <span class="bold">1</span> of 6</span>
      <span>Candidate: <span class="bold">SAMARTH KALE (ADT23SOCB0955)</span></span>
    </div>
  </div>

  <!-- ==================== PAGE 2: DATASET & TECHNOLOGY STACK ==================== -->
  <div class="report-page">
    <div class="institution-header">
      <div>
        <div class="inst-title">Department of Artificial Intelligence & Data Science</div>
        <div class="inst-sub">Dataset Specification & Technology Stack Comparative Analysis</div>
      </div>
      <div class="exam-badge">Activity-1 Report</div>
    </div>

    <!-- 3. DATASET -->
    <h2 class="sec-title"><span class="num">3</span> Dataset Specification & Agronomic Justification</h2>
    <table class="content-table">
      <thead>
        <tr>
          <th style="width: 22%;">Attribute</th>
          <th style="width: 38%;">Dataset Specification</th>
          <th style="width: 40%;">Agronomic Justification & Physical Role</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Dataset File</strong></td>
          <td><code>data/irrigation_sensor_data.csv</code></td>
          <td>2,500 balanced chronological observation records.</td>
        </tr>
        <tr>
          <td><strong>Input Features</strong></td>
          <td>
            1. <code>soil_moisture_percent</code> (0.0% to 100.0%)<br>
            2. <code>temperature_c</code> (-5.0°C to 50.0°C)<br>
            3. <code>humidity_percent</code> (10.0% to 100.0%)<br>
            4. <code>rainfall_mm</code> (0.0mm to 120.0mm)
          </td>
          <td>Derived from physical FAO-56 Penman-Monteith Evapotranspiration equations capturing soil matric suction, thermal energy, vapor pressure deficit, and rainfall replenishment.</td>
        </tr>
        <tr>
          <td><strong>Target Label</strong></td>
          <td><code>irrigation_needed</code> &isin; {{0, 1}}</td>
          <td>0 = Conserve (Valve Closed) | 1 = Irrigate (Valve Open).</td>
        </tr>
        <tr>
          <td><strong>Partition Method</strong></td>
          <td>80% Train (2,000) / 20% Held-Out Test (500)</td>
          <td>Stratified chronological partition with zero target leakage.</td>
        </tr>
        <tr>
          <td><strong>Rain Suppression</strong></td>
          <td>24-Hour Precipitation Threshold</td>
          <td>Suppresses irrigation during or immediately after rain events to prevent saturation waterlogging.</td>
        </tr>
      </tbody>
    </table>

    <!-- 4. TECHNOLOGY STACK -->
    <h2 class="sec-title"><span class="num">4</span> Technology Stack Comparative Analysis</h2>
    <table class="content-table">
      <thead>
        <tr>
          <th style="width: 20%;">Technology</th>
          <th style="width: 16%;">Domain</th>
          <th style="width: 26%;">Role in AgriSense System</th>
          <th style="width: 38%;">Why Selected Over Other Alternatives</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Python 3.10+</strong></td>
          <td>Core Runtime</td>
          <td>ML Pipeline & Inference Engine</td>
          <td>Comprehensive scientific ecosystem, native C-bindings, portable edge support.</td>
        </tr>
        <tr>
          <td><strong>scikit-learn</strong></td>
          <td>ML Framework</td>
          <td>StandardScaler + RandomForest</td>
          <td>Deterministic inference, resists overfitting, compact serialized artifact (&lt;1 MB).</td>
        </tr>
        <tr>
          <td><strong>FastAPI</strong></td>
          <td>REST API</td>
          <td>Asynchronous Edge Gateway Service</td>
          <td>High throughput, Pydantic type validation, automated OpenAPI documentation.</td>
        </tr>
        <tr>
          <td><strong>SQLite 3</strong></td>
          <td>Database</td>
          <td>Local Edge Event & Telemetry Ledger</td>
          <td>Serverless, zero configuration, atomic writes, zero RAM footprint.</td>
        </tr>
        <tr>
          <td><strong>React 19 + TypeScript</strong></td>
          <td>Frontend</td>
          <td>Farm Command Centre Dashboard</td>
          <td>Component modularity, strong static typing, ultra-fast UI re-renders.</td>
        </tr>
        <tr>
          <td><strong>Three.js / R3F</strong></td>
          <td>3D Visualization</td>
          <td>Interactive 3D Field Digital Twin</td>
          <td>Direct WebGL hardware acceleration, dynamic sector inspection, farmer avatar.</td>
        </tr>
        <tr>
          <td><strong>Azure Machine Learning</strong></td>
          <td>Cloud MLOps</td>
          <td>Model Registry & Version Governance</td>
          <td>Centralized cloud tracking (<code>smart-irrigation-edge-rf:1</code>) for edge deployment.</td>
        </tr>
      </tbody>
    </table>

    <div class="page-footer">
      <span>Activity-1: Smart Irrigation Edge AI • Practical-Based Assessment (PBA-2)</span>
      <span>Page <span class="bold">2</span> of 6</span>
      <span>Candidate: <span class="bold">SAMARTH KALE (ADT23SOCB0955)</span></span>
    </div>
  </div>

  <!-- ==================== PAGE 3: WORKFLOW, EVALUATION & CLOUD ==================== -->
  <div class="report-page">
    <div class="institution-header">
      <div>
        <div class="inst-title">Department of Artificial Intelligence & Data Science</div>
        <div class="inst-sub">Implementation Workflow, Model Evaluation & Cloud Integration</div>
      </div>
      <div class="exam-badge">Activity-1 Report</div>
    </div>

    <!-- 5. IMPLEMENTATION WORKFLOW -->
    <h2 class="sec-title"><span class="num">5</span> Step-by-Step Implementation Workflow</h2>
    <div class="flow-box">
      <div class="flow-step">
        <span class="num">Step 1</span>
        <div><strong>Data Ingestion & Preprocessing:</strong> Generated 2,500 balanced records with physical sensor ranges; configured <code>StandardScaler</code> to normalize multi-modal feature distributions.</div>
      </div>
      <div class="flow-step">
        <span class="num">Step 2</span>
        <div><strong>Model Training & Validation:</strong> Trained a 100-tree Random Forest classifier achieving 88.20% accuracy on 500 held-out test samples; serialized to <code>models/irrigation_model.joblib</code>.</div>
      </div>
      <div class="flow-step">
        <span class="num">Step 3</span>
        <div><strong>Azure ML Registration:</strong> Executed <code>register_azure_model.py</code> to register model version 1 into Azure ML Workspace <code>ml-assignment5-samarthkale</code>.</div>
      </div>
      <div class="flow-step">
        <span class="num">Step 4</span>
        <div><strong>Edge Engine & Validation Traps:</strong> Deployed <code>edge_inference.py</code> with physical guardrails (rejecting corrupted analog payloads) and SQLite telemetry persistence.</div>
      </div>
      <div class="flow-step">
        <span class="num">Step 5</span>
        <div><strong>FastAPI Service & 3D Dashboard:</strong> Started FastAPI on port 8000 and Vite React 19 on port 5173 featuring interactive 3D field sectors, live sliders, and time-series charts.</div>
      </div>
    </div>

    <!-- 6. EVALUATION RESULTS -->
    <h2 class="sec-title"><span class="num">6</span> Model Performance & Held-Out Test Verification</h2>

    <div class="metrics-row">
      <div class="metric-card accent">
        <div class="label">Test Accuracy</div>
        <div class="value">88.20%</div>
        <div class="sub">441 / 500 Correct</div>
      </div>
      <div class="metric-card accent">
        <div class="label">Test Precision</div>
        <div class="value">90.20%</div>
        <div class="sub">Water Waste Minimized</div>
      </div>
      <div class="metric-card">
        <div class="label">Test Recall</div>
        <div class="value">82.51%</div>
        <div class="sub">Deficits Captured</div>
      </div>
      <div class="metric-card">
        <div class="label">Test F1-Score</div>
        <div class="value">86.18%</div>
        <div class="sub">Optimal Balance</div>
      </div>
      <div class="metric-card">
        <div class="label">Edge Latency</div>
        <div class="value">74.8 ms</div>
        <div class="sub">Sub-100ms In-situ</div>
      </div>
    </div>

    <table class="content-table">
      <thead>
        <tr>
          <th>Actual Class \\ Model Prediction</th>
          <th>Predicted: Conserve (Valve Closed)</th>
          <th>Predicted: Irrigate (Valve Open)</th>
          <th>Category Total</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Actual: Moisture Adequate (0)</strong></td>
          <td><strong>257 (True Negatives - TN)</strong></td>
          <td>20 (False Positives - FP)</td>
          <td>277</td>
        </tr>
        <tr>
          <td><strong>Actual: Water Deficit (1)</strong></td>
          <td>39 (False Negatives - FN)</td>
          <td><strong>184 (True Positives - TP)</strong></td>
          <td>223</td>
        </tr>
      </tbody>
    </table>

    <p style="font-size: 8.2pt; margin-bottom: 8px;">
      <strong>Statistical Diagnostics:</strong> Specificity = <strong>92.8%</strong> | Sensitivity = <strong>82.5%</strong> | False Alarm Rate = <strong>7.2%</strong>.<br>
      <strong>Gini Feature Importances:</strong> <code>soil_moisture_percent: 68.69%</code> | <code>rainfall_mm: 17.36%</code> | <code>humidity_percent: 7.61%</code> | <code>temperature_c: 6.35%</code>.
    </p>

    <!-- 7. AZURE ML INTEGRATION -->
    <h2 class="sec-title"><span class="num">7</span> Azure Machine Learning Cloud Integration Details</h2>
    <table class="content-table">
      <thead>
        <tr>
          <th>Parameter</th>
          <th>Azure Configuration Value</th>
          <th>Operational Purpose</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Azure Subscription</strong></td>
          <td><code>6e2fed37-f192-4da5-9cc7-c4d5ede66b7f</code> (Azure for Students)</td>
          <td>Cloud resource billing and authentication.</td>
        </tr>
        <tr>
          <td><strong>Resource Group</strong></td>
          <td><code>rg-ml-assignment</code></td>
          <td>Centralized asset container.</td>
        </tr>
        <tr>
          <td><strong>ML Workspace</strong></td>
          <td><code>ml-assignment5-samarthkale</code></td>
          <td>Target enterprise ML workspace.</td>
        </tr>
        <tr>
          <td><strong>Registered Model</strong></td>
          <td><code>smart-irrigation-edge-rf</code> (Version 1)</td>
          <td>Audited model artifact available for edge fleet synchronization.</td>
        </tr>
      </tbody>
    </table>

    <div class="page-footer">
      <span>Activity-1: Smart Irrigation Edge AI • Practical-Based Assessment (PBA-2)</span>
      <span>Page <span class="bold">3</span> of 6</span>
      <span>Candidate: <span class="bold">SAMARTH KALE (ADT23SOCB0955)</span></span>
    </div>
  </div>

  <!-- ==================== PAGE 4: VISUAL DEMO PART 1 ==================== -->
  <div class="report-page">
    <div class="institution-header">
      <div>
        <div class="inst-title">Department of Artificial Intelligence & Data Science</div>
        <div class="inst-sub">Visual Demonstration & Live Operational System Evidence (Part 1)</div>
      </div>
      <div class="exam-badge">Activity-1 Report</div>
    </div>

    <h2 class="sec-title"><span class="num">8</span> Visual System Evidence: Operational 3D Twin & Telemetry Simulator</h2>

    <div class="shot-card">
      <img src="{img1}" alt="Farm Overview 3D Digital Twin">
      <div class="shot-caption">
        <span><span class="fig-id">Figure 1:</span> Farm Command Centre & Interactive 3D Digital Twin</span>
        <span>Moisture: 44% • Actuator: VALVE_CLOSED (74.8ms)</span>
      </div>
      <div class="shot-desc">
        Demonstrates the real-time Three.js WebGL digital twin displaying 4 crop sectors (Wheat, Corn, Soybeans, Barley), live sensor telemetry cards, water storage level monitoring, and the offline Edge AI prediction indicating moisture adequacy with the valve closed.
      </div>
    </div>

    <div class="shot-card">
      <img src="{img2}" alt="Live Telemetry Simulator">
      <div class="shot-caption">
        <span><span class="fig-id">Figure 2:</span> Live IoT Telemetry Simulator & Precision Calibrator</span>
        <span>Scenario Presets & Actuator Testing (Confidence: 65.5%)</span>
      </div>
      <div class="shot-desc">
        Demonstrates the interactive calibration suite featuring rapid scenario presets (Drought Stress, Adequate Post-Rain, Midday Heat Spike), manual input override sliders, and immediate Edge AI inference probability feedback with actuator actuation testing.
      </div>
    </div>

    <div class="page-footer">
      <span>Activity-1: Smart Irrigation Edge AI • Practical-Based Assessment (PBA-2)</span>
      <span>Page <span class="bold">4</span> of 6</span>
      <span>Candidate: <span class="bold">SAMARTH KALE (ADT23SOCB0955)</span></span>
    </div>
  </div>

  <!-- ==================== PAGE 5: VISUAL DEMO PART 2 ==================== -->
  <div class="report-page">
    <div class="institution-header">
      <div>
        <div class="inst-title">Department of Artificial Intelligence & Data Science</div>
        <div class="inst-sub">Visual Demonstration & Live Operational System Evidence (Part 2)</div>
      </div>
      <div class="exam-badge">Activity-1 Report</div>
    </div>

    <h2 class="sec-title"><span class="num">9</span> Visual System Evidence: Field Sector Inspection & Telemetry Analytics</h2>

    <div class="shot-card">
      <img src="{img3}" alt="3D Field Sector Zoom">
      <div class="shot-caption">
        <span><span class="fig-id">Figure 3:</span> 3D Field Sector Zoom & Patrolling Farmer Avatar</span>
        <span>Sector 4 (Barley) • In-situ Sensor Inspection</span>
      </div>
      <div class="shot-desc">
        Demonstrates interactive camera navigation zooming into Sector 4 (Barley), displaying procedural crop row rendering, dynamic watering states, the autonomous farmer avatar, and localized micro-climate telemetry inspection.
      </div>
    </div>

    <div class="shot-card">
      <img src="{img4}" alt="Telemetry History">
      <div class="shot-caption">
        <span><span class="fig-id">Figure 4:</span> Edge Telemetry History & Time-Series Sensor Dynamics</span>
        <span>Multi-Sensor Dynamics vs. 20% Wilting Threshold</span>
      </div>
      <div class="shot-desc">
        Demonstrates chronological multi-sensor trend lines rendered from the local SQLite edge database, tracking Relative Humidity, Soil Moisture, and Canopy Temperature against the critical 20% permanent crop wilting threshold.
      </div>
    </div>

    <div class="page-footer">
      <span>Activity-1: Smart Irrigation Edge AI • Practical-Based Assessment (PBA-2)</span>
      <span>Page <span class="bold">5</span> of 6</span>
      <span>Candidate: <span class="bold">SAMARTH KALE (ADT23SOCB0955)</span></span>
    </div>
  </div>

  <!-- ==================== PAGE 6: VISUAL DEMO PART 3, CONCLUSION & REPO ==================== -->
  <div class="report-page">
    <div class="institution-header">
      <div>
        <div class="inst-title">Department of Artificial Intelligence & Data Science</div>
        <div class="inst-sub">Scientific Verification, Cloud Registry & Final Conclusion</div>
      </div>
      <div class="exam-badge">Activity-1 Report</div>
    </div>

    <div class="shot-card" style="margin-top: 4px;">
      <img src="{img5}" alt="Model Evaluation" style="max-height: 195px;">
      <div class="shot-caption">
        <span><span class="fig-id">Figure 5:</span> Held-Out Test Split Model Evaluation & Verification</span>
        <span>88.20% Accuracy • Confusion Matrix • Gini Feature Distribution</span>
      </div>
    </div>

    <div class="shot-card" style="margin-top: 6px;">
      <img src="{img6}" alt="Azure ML Model Registry" style="max-height: 195px;">
      <div class="shot-caption">
        <span><span class="fig-id">Figure 6:</span> Microsoft Azure Machine Learning Studio Model Registry</span>
        <span>Model 'smart-irrigation-edge-rf:1' in Workspace 'ml-assignment5-samarthkale'</span>
      </div>
    </div>

    <!-- 10. CONCLUSION & GITHUB -->
    <h2 class="sec-title" style="margin-top: 8px;"><span class="num">10</span> Conclusion & Practical Examination Takeaways</h2>
    <p style="font-size: 8.3pt; margin-bottom: 4px;">
      The <strong>AgriSense Edge AI</strong> project demonstrates a complete, production-ready cyber-physical architecture:
    </p>
    <ul style="font-size: 8.2pt; margin-bottom: 6px;">
      <li><strong>Water Stewardship:</strong> Eliminates up to 35% of irrigation water waste through real-time predictive solenoid valve actuation.</li>
      <li><strong>Edge Autonomy:</strong> The local edge engine functions 100% offline with sub-75ms latency, safeguarding crops during rural cellular blackouts.</li>
      <li><strong>Enterprise Cloud Sync:</strong> Azure Machine Learning Studio provides centralized model versioning (<code>smart-irrigation-edge-rf:1</code>) for scalable fleet governance.</li>
    </ul>

    <div class="flow-box" style="margin-top: 6px; padding: 6px 12px; text-align: center;">
      <strong>Official GitHub Repository:</strong> <a href="https://github.com/SamarthKale5556/SmartAgri-Edge-AI" style="color: #0284c7; text-decoration: none; font-weight: 700;">https://github.com/SamarthKale5556/SmartAgri-Edge-AI</a><br>
      <span style="font-size: 8pt; color: #64748b;">Authored by SAMARTH KALE • Enrollment: ADT23SOCB0955 • Div: AIEC02 • Roll No: 37</span>
    </div>

    <div class="page-footer">
      <span>Activity-1: Smart Irrigation Edge AI • Practical-Based Assessment (PBA-2)</span>
      <span>Page <span class="bold">6</span> of 6</span>
      <span>Candidate: <span class="bold">SAMARTH KALE (ADT23SOCB0955)</span></span>
    </div>
  </div>

</body>
</html>
"""

with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[HTML GENERATED] Saved styled HTML to: {HTML_OUTPUT}")

browser_exe = None
for p in EDGE_PATHS:
    if os.path.exists(p):
        browser_exe = p
        break

if browser_exe:
    print(f"[PDF COMPILER] Using browser: {browser_exe}")
    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={PDF_OUTPUT}",
        HTML_OUTPUT
    ]
    subprocess.run(cmd, check=True)
    if os.path.exists(PDF_OUTPUT):
        print(f"[PDF SUCCESS] Generated publication-grade PDF Report at: {PDF_OUTPUT} ({os.path.getsize(PDF_OUTPUT) / 1024:.1f} KB)")
else:
    print("[ERROR] Neither Microsoft Edge nor Google Chrome found.")
