"""
generate_pdf_report.py - Professional PDF Report Generator
Generates an executive-styled PDF report for Samarth Kale's Activity-1 submission
with styled tables, metrics, and embedded high-resolution screenshots.
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
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

  @page {{
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
  }}

  body {{
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    color: #1e293b;
    background: #ffffff;
    line-height: 1.55;
    font-size: 11pt;
    margin: 0;
    padding: 0;
  }}

  .header-card {{
    background: linear-gradient(135deg, #060B18 0%, #0F1A3A 100%);
    color: #ffffff;
    padding: 24px;
    border-radius: 12px;
    margin-bottom: 24px;
    border: 1px solid #38bdf8;
  }}

  .header-card h1 {{
    margin: 0 0 6px 0;
    font-size: 20pt;
    font-weight: 800;
    color: #38bdf8;
    letter-spacing: -0.5px;
  }}

  .header-card h2 {{
    margin: 0 0 16px 0;
    font-size: 13pt;
    font-weight: 500;
    color: #cbd5e1;
  }}

  .cred-table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 12px;
    background: rgba(255, 255, 255, 0.07);
    border-radius: 8px;
    overflow: hidden;
  }}

  .cred-table td {{
    padding: 7px 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    font-size: 10pt;
  }}

  .cred-table td.label {{
    color: #94a3b8;
    width: 25%;
    font-weight: 600;
  }}

  .cred-table td.val {{
    color: #f8fafc;
    font-weight: 700;
  }}

  h2.section-title {{
    font-size: 14pt;
    font-weight: 700;
    color: #0f172a;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 6px;
    margin-top: 26px;
    margin-bottom: 14px;
  }}

  p, li {{
    color: #334155;
    font-size: 10.5pt;
  }}

  table.data-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 10pt;
  }}

  table.data-table th {{
    background: #0f172a;
    color: #ffffff;
    padding: 9px 12px;
    text-align: left;
    font-weight: 600;
  }}

  table.data-table td {{
    padding: 8px 12px;
    border-bottom: 1px solid #e2e8f0;
    color: #334155;
  }}

  table.data-table tr:nth-child(even) {{
    background: #f8fafc;
  }}

  .metric-grid {{
    display: flex;
    gap: 12px;
    margin: 16px 0;
  }}

  .metric-box {{
    flex: 1;
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 12px;
    text-align: center;
  }}

  .metric-box.highlight {{
    background: #ecfdf5;
    border-color: #10b981;
  }}

  .metric-box .label {{
    font-size: 8.5pt;
    text-transform: uppercase;
    font-weight: 700;
    color: #64748b;
  }}

  .metric-box .val {{
    font-size: 16pt;
    font-weight: 800;
    color: #0f172a;
    margin: 4px 0;
    font-family: 'JetBrains Mono', monospace;
  }}

  .metric-box .sub {{
    font-size: 8pt;
    color: #059669;
    font-weight: 600;
  }}

  .screenshot-container {{
    margin: 18px 0;
    page-break-inside: avoid;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    overflow: hidden;
    background: #060B18;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  }}

  .screenshot-container img {{
    width: 100%;
    display: block;
  }}

  .screenshot-caption {{
    background: #0f172a;
    color: #38bdf8;
    font-size: 9pt;
    padding: 7px 12px;
    font-weight: 600;
    border-top: 1px solid #1e293b;
  }}

  .page-break {{
    page-break-before: always;
  }}

  .badge {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 8.5pt;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
  }}

  .badge-green {{ background: #dcfce7; color: #15803d; }}
  .badge-blue {{ background: #e0f2fe; color: #0369a1; }}
  .badge-amber {{ background: #fef3c7; color: #b45309; }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    background: #f1f5f9;
    color: #0369a1;
    padding: 1px 5px;
    border-radius: 4px;
    font-size: 9pt;
  }}
</style>
</head>
<body>

  <!-- Cover Card -->
  <div class="header-card">
    <h1>🌾 SMART AGRICULTURE IRRIGATION SYSTEM (EDGE AI)</h1>
    <h2>PBA-2 Practical Examination Report • Activity-1 Submission</h2>
    
    <table class="cred-table">
      <tr>
        <td class="label">STUDENT NAME</td>
        <td class="val">SAMARTH KALE</td>
        <td class="label">ENROLLMENT NO</td>
        <td class="val">ADT23SOCB0955</td>
      </tr>
      <tr>
        <td class="label">DIVISION / ROLL NO</td>
        <td class="val">AIEC02 / Roll No: 37</td>
        <td class="label">TARGET WORKSPACE</td>
        <td class="val">Samarth Kale's Workspace</td>
      </tr>
      <tr>
        <td class="label">AZURE ML WORKSPACE</td>
        <td class="val">ml-assignment5-samarthkale</td>
        <td class="label">MODEL ASSET ID</td>
        <td class="val">smart-irrigation-edge-rf:1</td>
      </tr>
      <tr>
        <td class="label">GITHUB REPO</td>
        <td class="val" colspan="3">https://github.com/SamarthKale5556/SmartAgri-Edge-AI</td>
      </tr>
    </table>
  </div>

  <!-- 1. Aim -->
  <h2 class="section-title">1. Aim of the Project</h2>
  <p>
    To engineer, train, and deploy an <strong>autonomous Edge Machine Learning system</strong> that predicts real-time agricultural crop irrigation needs (<code>VALVE_OPEN</code> vs <code>VALVE_CLOSED</code>) from multi-sensor telemetry (Soil Moisture, Canopy Temperature, Relative Humidity, and Precipitation), achieving <strong>sub-100 millisecond inference latency</strong> with 100% offline edge reliability while synchronizing model lifecycle management via <strong>Azure Machine Learning Studio</strong>.
  </p>

  <!-- 2. Theory -->
  <h2 class="section-title">2. Theoretical Foundation & Problem Formulation</h2>
  <p>
    Conventional agriculture relies on rigid timer-based irrigation, causing two major failures:
  </p>
  <ul>
    <li><strong>Over-Irrigation:</strong> Excess water causes root-zone hypoxia (root rot), leaches soil nitrates into groundwater, and wastes up to 35% of fresh water.</li>
    <li><strong>Under-Irrigation:</strong> Water stress causes stomatal closure, reducing crop yield and plant health.</li>
    <li><strong>The Rural Connectivity Barrier:</strong> Remote farmland frequently suffers from intermittent or absent internet connectivity. Pure cloud-based AI fails during connectivity loss.</li>
  </ul>
  <p>
    <strong>The Edge AI Solution:</strong> We deploy a trained <strong>Random Forest Classifier</strong> pipeline directly onto the local edge gateway. The edge node samples physical sensors, validates payloads, predicts irrigation need in 74.8 ms, and signals the solenoid valve relay completely offline.
  </p>

  <!-- 3. Dataset -->
  <h2 class="section-title">3. Dataset: Selection & Agronomic Justification</h2>
  <table class="data-table">
    <thead>
      <tr>
        <th>Attribute</th>
        <th>Dataset Specification</th>
        <th>Agronomic Justification</th>
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
        <td>Soil Moisture (%), Temperature (°C), Humidity (%), Rainfall (mm)</td>
        <td>Derived from FAO-56 Penman-Monteith Evapotranspiration dynamics.</td>
      </tr>
      <tr>
        <td><strong>Target Label</strong></td>
        <td><code>irrigation_needed</code> (0 = Conserve, 1 = Irrigate)</td>
        <td>Binary decision mapped directly to the solenoid relay valve.</td>
      </tr>
      <tr>
        <td><strong>Split Method</strong></td>
        <td>80% Train (2,000 samples) / 20% Held-Out Test (500 samples)</td>
        <td>Stratified, zero target leakage, strictly tested on unseen samples.</td>
      </tr>
      <tr>
        <td><strong>Rain Suppression</strong></td>
        <td>24h Cumulative Precipitation Window</td>
        <td>Prevents wasteful irrigation when recent rainfall has occurred.</td>
      </tr>
    </tbody>
  </table>

  <!-- Page Break -->
  <div class="page-break"></div>

  <!-- 4. Technology Stack Matrix -->
  <h2 class="section-title">4. Technology Stack Comparison Matrix</h2>
  <table class="data-table">
    <thead>
      <tr>
        <th>Technology</th>
        <th>Category</th>
        <th>Role in AgriSense</th>
        <th>Advantage Over Alternative Options</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>scikit-learn</strong></td>
        <td>Machine Learning</td>
        <td>Random Forest Classifier</td>
        <td>Compact footprint (&lt;1 MB), sub-100ms inference on low-power ARM/x86 gateways.</td>
      </tr>
      <tr>
        <td><strong>FastAPI</strong></td>
        <td>Backend Framework</td>
        <td>Edge Telemetry API</td>
        <td>High-speed asynchronous Python server with native Swagger / OpenAPI documentation.</td>
      </tr>
      <tr>
        <td><strong>SQLite 3</strong></td>
        <td>Embedded Storage</td>
        <td>Edge Event Ledger</td>
        <td>Zero-configuration, serverless, atomic logging with instant CSV export.</td>
      </tr>
      <tr>
        <td><strong>React 19 + TypeScript</strong></td>
        <td>Frontend Framework</td>
        <td>Command Centre UI</td>
        <td>Strong typing, reactive state management, high reliability.</td>
      </tr>
      <tr>
        <td><strong>Three.js / R3F</strong></td>
        <td>3D Graphics</td>
        <td>Farm Digital Twin</td>
        <td>Hardware-accelerated 3D rendering of crop rows, water tank, and patrolling farmer avatar.</td>
      </tr>
      <tr>
        <td><strong>Azure Machine Learning</strong></td>
        <td>Cloud MLOps</td>
        <td>Model Registry</td>
        <td>Centralized model versioning (<code>smart-irrigation-edge-rf:1</code>), enterprise governance.</td>
      </tr>
    </tbody>
  </table>

  <!-- 5. Evaluation Metrics -->
  <h2 class="section-title">5. Model Performance & Held-Out Test Verification</h2>
  
  <div class="metric-grid">
    <div class="metric-box highlight">
      <div class="label">Test Accuracy</div>
      <div class="val">88.20%</div>
      <div class="sub">441 of 500 Correct</div>
    </div>
    <div class="metric-box highlight">
      <div class="label">Test Precision</div>
      <div class="val">90.20%</div>
      <div class="sub">Low False Alarms</div>
    </div>
    <div class="metric-box">
      <div class="label">Test Recall</div>
      <div class="val">82.51%</div>
      <div class="sub">Deficit Captured</div>
    </div>
    <div class="metric-box">
      <div class="label">Test F1-Score</div>
      <div class="val">86.18%</div>
      <div class="sub">Harmonic Balance</div>
    </div>
  </div>

  <table class="data-table">
    <thead>
      <tr>
        <th>Actual Class \\ Model Prediction</th>
        <th>Predicted: Conserve (Valve Closed)</th>
        <th>Predicted: Irrigate (Valve Open)</th>
        <th>Total Observations</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Actual: Moisture Adequate (0)</strong></td>
        <td><strong>257 (True Negatives)</strong></td>
        <td>20 (False Positives)</td>
        <td>277</td>
      </tr>
      <tr>
        <td><strong>Actual: Water Deficit (1)</strong></td>
        <td>39 (False Negatives)</td>
        <td><strong>184 (True Positives)</strong></td>
        <td>223</td>
      </tr>
    </tbody>
  </table>

  <p>
    <strong>Feature Importances (Gini Impurity):</strong> 
    <code>soil_moisture_percent: 68.69%</code> | 
    <code>rainfall_mm: 17.36%</code> | 
    <code>humidity_percent: 7.61%</code> | 
    <code>temperature_c: 6.35%</code>
  </p>

  <!-- Page Break for Visual Evidence -->
  <div class="page-break"></div>

  <!-- 6. Visual Evidence & Screenshots -->
  <h2 class="section-title">6. Visual Demonstration & Live System Screenshots</h2>

  <div class="screenshot-container">
    <img src="{img1}" alt="3D Farm Overview">
    <div class="screenshot-caption">Figure 1: Farm Command Centre & 3D Digital Twin — Real-time sector health, moisture card (44%), and VALVE_CLOSED actuation.</div>
  </div>

  <div class="screenshot-container">
    <img src="{img2}" alt="Live Telemetry Simulator">
    <div class="screenshot-caption">Figure 2: Live IoT Telemetry Simulator & Precision Calibrator — Manual slider override & edge inference response (146ms).</div>
  </div>

  <div class="page-break"></div>

  <div class="screenshot-container">
    <img src="{img3}" alt="Field Sector Zoom">
    <div class="screenshot-caption">Figure 3: Interactive 3D Field Sector Zoom — Detailed inspection of Sector 4 (Barley) with patrolling farmer avatar.</div>
  </div>

  <div class="screenshot-container">
    <img src="{img4}" alt="Telemetry History">
    <div class="screenshot-caption">Figure 4: Edge Telemetry History & Time-Series Dynamics — Multi-variable trends vs. critical threshold and SQLite audit log.</div>
  </div>

  <div class="page-break"></div>

  <div class="screenshot-container">
    <img src="{img5}" alt="Model Evaluation">
    <div class="screenshot-caption">Figure 5: Held-Out Test Split Model Evaluation — 88.20% Accuracy, 257 TN / 184 TP Confusion Matrix, and Gini Feature Breakdown.</div>
  </div>

  <div class="screenshot-container">
    <img src="{img6}" alt="Azure ML Studio Registration">
    <div class="screenshot-caption">Figure 6: Azure Machine Learning Studio Model Registry — Model 'smart-irrigation-edge-rf:1' successfully registered in workspace ml-assignment5-samarthkale.</div>
  </div>

  <!-- 7. Conclusion -->
  <h2 class="section-title">7. Conclusion & Viva Takeaways</h2>
  <p>
    The <strong>AgriSense Edge AI</strong> system successfully bridges theoretical machine learning and practical industrial agricultural engineering.
  </p>
  <ul>
    <li><strong>Precision Water Stewardship:</strong> Autonomous valve actuation cuts agricultural water consumption by up to 35%.</li>
    <li><strong>Edge Reliability:</strong> By hosting inference locally, valve control never halts due to rural cellular internet dropouts.</li>
    <li><strong>Cloud Governance:</strong> Integration with <strong>Azure Machine Learning Studio</strong> provides centralized artifact versioning, creating a complete Cloud-to-Edge MLOps v2 template.</li>
  </ul>

  <div style="margin-top: 24px; padding: 12px; background: #f1f5f9; border-radius: 8px; text-align: center; font-size: 9.5pt; color: #475569;">
    <strong>Candidate: SAMARTH KALE</strong> • Enrollment: ADT23SOCB0955 • Div: AIEC02 • Roll No: 37 • MIT World Peace University
  </div>

</body>
</html>
"""

with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[HTML GENERATED] Saved styled HTML to: {HTML_OUTPUT}")

# Convert HTML to PDF using Headless Edge
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
        print(f"[PDF SUCCESS] Generated PDF Report at: {PDF_OUTPUT} ({os.path.getsize(PDF_OUTPUT) / 1024:.1f} KB)")
else:
    print("[ERROR] Neither Microsoft Edge nor Google Chrome found for headless PDF printing.")
