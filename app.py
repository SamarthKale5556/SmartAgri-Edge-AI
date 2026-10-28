"""
app.py - Real-Time Smart Agriculture Edge Dashboard
Domain: Smart Agriculture: Real-Time Irrigation Prediction at the IoT Edge

Built with Streamlit, Plotly, scikit-learn, and SQLite.
Local edge-style inference with optional Azure Machine Learning model registration.
"""

import os
import json
import sqlite3
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime

from edge_inference import get_edge_engine, DB_PATH, MODEL_PATH
from simulate_iot import IoTSensorSimulator, SCENARIOS
from register_azure_model import check_azure_status

# Page setup
st.set_page_config(
    page_title="SmartAgri Edge | IoT Irrigation Predictor",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Modern Aesthetic CSS
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    code, pre {
        font-family: 'JetBrains+Mono', monospace !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* Gradient Header Banner */
    .header-banner {
        background: linear-gradient(135deg, #0d3b2e 0%, #115e59 50%, #064e3b 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: #f0fdf4;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(6, 78, 59, 0.25);
        border: 1px solid rgba(52, 211, 153, 0.2);
    }
    .header-title {
        font-size: 1.85rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
        color: #ffffff;
    }
    .header-subtitle {
        font-size: 0.95rem;
        color: #a7f3d0;
        margin-top: 0.4rem;
        margin-bottom: 0;
    }

    /* Status Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .badge-edge {
        background-color: #064e3b;
        color: #6ee7b7;
        border: 1px solid #10b981;
    }
    .badge-synthetic {
        background-color: #451a03;
        color: #fcd34d;
        border: 1px solid #f59e0b;
    }
    .badge-cloud {
        background-color: #1e1b4b;
        color: #c7d2fe;
        border: 1px solid #6366f1;
    }

    /* Action Cards */
    .metric-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .metric-label {
        color: #9ca3af;
        font-size: 0.8rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        color: #f9fafb;
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 0.2rem;
    }

    /* Valve Status Banner */
    .valve-on {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(185, 28, 28, 0.2) 100%);
        border: 2px solid #ef4444;
        border-radius: 10px;
        padding: 1rem 1.5rem;
        color: #fca5a5;
    }
    .valve-off {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.2) 100%);
        border: 2px solid #10b981;
        border-radius: 10px;
        padding: 1rem 1.5rem;
        color: #6ee7b7;
    }

    /* Disclaimer box */
    .honesty-box {
        background: #1e1e24;
        border-left: 4px solid #f59e0b;
        padding: 0.75rem 1rem;
        border-radius: 4px;
        font-size: 0.85rem;
        color: #e5e7eb;
        margin: 1rem 0;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# Initialize Edge Engine & Simulator
@st.cache_resource
def load_cached_engine():
    return get_edge_engine()

try:
    engine = load_cached_engine()
except Exception as e:
    st.error(f"Failed to load edge model: {e}. Please ensure 'train_model.py' has completed.")
    st.stop()

simulator = IoTSensorSimulator()

# Top Navigation / Header
st.markdown("""
<div class="header-banner">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1 class="header-title">🌱 Smart Agriculture: IoT Edge Irrigation Predictor</h1>
            <p class="header-subtitle">Real-Time Sensor Telemetry • Local In-Situ ML Inference • Optional Azure ML Model Lifecycle</p>
        </div>
        <div style="display: flex; gap: 0.5rem; margin-top: 0.5rem;">
            <span class="badge badge-edge">⚡ Edge Runtime: Active</span>
            <span class="badge badge-synthetic">🔬 Dataset: Synthetic Agro-Heuristic</span>
            <span class="badge badge-cloud">☁️ Azure ML: Optional</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# Sidebar controls & system info
with st.sidebar:
    st.markdown("### 🎛️ Edge Node Controller")
    st.markdown(f"**Host Architecture:** Local Edge Node")
    st.markdown(f"**Model Artifact:** `irrigation_model.joblib`")
    st.markdown(f"**Telemetry Storage:** SQLite (`edge_telemetry.db`)")
    st.markdown(f"**Engine Init Latency:** `{engine.load_time_ms} ms`")
    st.markdown("---")

    st.markdown("### ⚡ Quick Presets")
    selected_scenario = st.selectbox(
        "Load Agricultural Condition:",
        options=list(SCENARIOS.keys()),
        index=0
    )
    st.caption(SCENARIOS[selected_scenario]["description"])

    st.markdown("---")
    st.markdown("### 📌 Practical Exam Guide")
    st.info(
        "**PBA-2 Flow:**\n"
        "1. Overview & Data Flow\n"
        "2. Live IoT Simulation\n"
        "3. Held-out Model Evaluation\n"
        "4. Telemetry History & Export\n"
        "5. Azure ML & Edge Architecture"
    )


# 5 Main Sections (Tabs)
tab_overview, tab_sim, tab_eval, tab_history, tab_azure = st.tabs([
    "📋 Overview & Architecture",
    "📡 Live IoT Simulation",
    "📊 Model Evaluation",
    "📈 Prediction History & Trends",
    "☁️ Azure ML & Edge Lifecycle"
])


# ==========================================
# TAB 1: OVERVIEW & ARCHITECTURE
# ==========================================
with tab_overview:
    st.markdown("### 🎯 Problem Statement & Edge Solution")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("""
        **The Agricultural Challenge:**
        Crop fields require timely, precise irrigation. Under-watering induces drought stress and yield loss,
        while over-watering wastes critical water resources, leaches soil nutrients, and causes root rot.
        Manual field inspection is labor-intensive, slow, and cannot scale across multi-acre plots.
        """)
    with col_p2:
        st.markdown("""
        **The IoT Edge Solution:**
        Low-power IoT sensors capture volumetric soil moisture, ambient temperature, relative humidity,
        and rainfall. An embedded **scikit-learn Random Forest classifier** executes **in-situ on the edge device**,
        evaluating soil water deficit against atmospheric evaporative demand and actuating irrigation valves in **< 100 ms**
        without internet or cloud dependency.
        """)

    st.markdown("---")
    st.markdown("### 🔄 End-to-End System Architecture & Data Flow")

    arch_diagram = """
    ```mermaid
    graph LR
        subgraph IoT Edge Node [IoT Field Node / Edge Gateway]
            S1[Soil Moisture Sensor] --> VAL[Input Validation & Plausibility Check]
            S2[Ambient Temp Sensor] --> VAL
            S3[Air Humidity Sensor] --> VAL
            S4[Rainfall Gauge] --> VAL
            VAL --> INF[Local Edge Inference Engine]
            MDL[(Local Model Artifact: irrigation_model.joblib)] --> INF
            INF --> ACT{Actuator Directive}
            ACT -->|Pred = 1| V_ON[VALVE_OPEN: Trigger Irrigation]
            ACT -->|Pred = 0| V_OFF[VALVE_CLOSED: Conserve Water]
            INF --> LDB[(Local SQLite DB: edge_telemetry.db)]
        end

        subgraph Cloud ML Lifecycle [Optional Azure Machine Learning Cloud]
            DS[(Synthetic Agro Dataset)] --> AZ_TRN[Azure ML Training Workspace]
            AZ_TRN --> AZ_REG[Model Registry: Versioned Asset]
            AZ_REG -.->|Optional Deploy / Sync| MDL
        end
    ```
    """
    st.markdown(arch_diagram)

    st.markdown("---")
    st.markdown("### 🔍 Model & Runtime Status")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label="Edge Inference Status", value="ONLINE", delta="Zero Cloud Dependency")
    with c2:
        st.metric(label="Model Architecture", value="Random Forest", delta="StandardScaler + RF (100 Trees)")
    with c3:
        st.metric(label="Dataset Type", value="Synthetic Heuristic", delta="Fixed Seed = 42")
    with c4:
        st.metric(label="Actuator Protocol", value="Local Direct Call", delta="Sub-100ms Reaction")

    # Fetch latest reading from history
    hist = engine.get_history_df(limit=1)
    if not hist.empty:
        latest = hist.iloc[0]
        st.markdown("#### ⏱️ Most Recent Edge Event")
        latest_cols = st.columns(5)
        latest_cols[0].metric("Timestamp", latest["timestamp"])
        latest_cols[1].metric("Soil Moisture", f"{latest['soil_moisture']}%")
        latest_cols[2].metric("Temperature", f"{latest['temperature']} °C")
        latest_cols[3].metric("Action", latest["action_code"])
        latest_cols[4].metric("Latency", f"{latest['latency_ms']} ms")


# ==========================================
# TAB 2: LIVE IOT SIMULATION
# ==========================================
with tab_sim:
    st.markdown("### 📡 Live IoT Telemetry Simulator & Edge Inference Engine")

    col_sim_ctrl, col_sim_view = st.columns([1, 1.4])

    with col_sim_ctrl:
        st.markdown("#### 1. Telemetry Generation Controls")
        st.markdown(f"Current Preset: **{selected_scenario}**")

        c_btn1, c_btn2 = st.columns(2)
        btn_single = c_btn1.button("⚡ Generate Single Reading", use_container_width=True, type="primary")
        btn_stream = c_btn2.button("🌊 Simulate Stream (5 Packets)", use_container_width=True)

        st.markdown("##### Or Override Sensor Inputs Manually:")
        with st.expander("🛠️ Manual Sensor Sliders (Interactive Testing)", expanded=False):
            manual_sm = st.slider("Soil Moisture (%)", min_value=0.0, max_value=100.0, value=22.0, step=0.5)
            manual_temp = st.slider("Ambient Temperature (°C)", min_value=-5.0, max_value=60.0, value=34.0, step=0.5)
            manual_hum = st.slider("Air Humidity (%)", min_value=5.0, max_value=100.0, value=30.0, step=0.5)
            manual_rain = st.slider("Recent Rainfall (mm)", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
            btn_manual = st.button("🚀 Run Inference on Manual Inputs", use_container_width=True)

    with col_sim_view:
        st.markdown("#### 2. Live Edge Prediction & Actuator Status")

        # Determine which action to run
        active_reading = None
        stream_results = None

        if btn_manual:
            active_reading = {
                "node_id": "IOT-NODE-MANUAL",
                "soil_moisture_percent": manual_sm,
                "temperature_c": manual_temp,
                "humidity_percent": manual_hum,
                "rainfall_mm": manual_rain,
                "scenario": "Manual User Override"
            }
        elif btn_single:
            active_reading = simulator.generate_reading(scenario_name=selected_scenario)
        elif btn_stream:
            stream_results = simulator.simulate_stream(num_readings=5)
            active_reading = stream_results[-1]["reading"]

        if active_reading:
            # Run actual inference
            res = engine.predict(active_reading, record_history=True)

            if not res["success"]:
                st.error(f"⚠️ **Edge Validation Alert**: {res['error']}")
                st.warning("Sensor reading was rejected before reaching the ML classifier. Actuator held in safe state.")
            else:
                pred = res["prediction"]
                prob = res["irrigation_probability"]
                conf = res["confidence_score"]
                latency = res["latency_ms"]
                action = res["action_code"]

                # Valve status visual
                if pred == 1:
                    st.markdown(f"""
                    <div class="valve-on">
                        <h3 style="margin:0; color:#ef4444;">🚨 IRRIGATION RECOMMENDED • ACTUATOR: {action}</h3>
                        <p style="margin:0.25rem 0 0 0; font-size:1.05rem;">{res['recommendation']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="valve-off">
                        <h3 style="margin:0; color:#10b981;">✅ MOISTURE ADEQUATE • ACTUATOR: {action}</h3>
                        <p style="margin:0.25rem 0 0 0; font-size:1.05rem;">{res['recommendation']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Sensor Cards
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Soil Moisture", f"{active_reading['soil_moisture_percent']}%", "Volumetric")
                m2.metric("Temperature", f"{active_reading['temperature_c']} °C", "Canopy Ambient")
                m3.metric("Humidity", f"{active_reading['humidity_percent']}%", "Relative")
                m4.metric("Rainfall", f"{active_reading['rainfall_mm']} mm", "Past 24h")

                st.markdown("---")
                p_col1, p_col2 = st.columns([1.5, 1])
                with p_col1:
                    st.markdown(f"**Calculated Irrigation Probability: `{prob * 100:.1f}%`**")
                    st.progress(prob)
                    st.markdown(f"**Classifier Confidence Score:** `{conf * 100:.1f}%` | **Edge Latency:** `{latency} ms`")

                with p_col2:
                    st.markdown("""
                    <div class="honesty-box" style="margin-top:0;">
                        <b>⚠️ Epistemic Limitation:</b><br>
                        Probability represents Random Forest tree vote consensus on synthetic training rules. It does not signify true physical soil hydraulic potential.
                    </div>
                    """, unsafe_allow_html=True)

        elif stream_results:
            st.success(f"Simulated and recorded a burst of 5 telemetry packets to SQLite!")
        else:
            st.info("👈 Click **'Generate Single Reading'**, select a preset, or test manual sliders to trigger live inference.")


# ==========================================
# TAB 3: MODEL EVALUATION
# ==========================================
with tab_eval:
    st.markdown("### 📊 Model Architecture & Held-Out Test Evaluation")

    metrics_file = os.path.join(os.path.dirname(__file__), "outputs", "evaluation_metrics.json")
    cm_img_file = os.path.join(os.path.dirname(__file__), "outputs", "confusion_matrix.png")

    if os.path.exists(metrics_file):
        with open(metrics_file, "r") as f:
            metrics = json.load(f)

        m_c1, m_c2, m_c3, m_c4 = st.columns(4)
        m_c1.metric("Test Accuracy", f"{metrics['test_accuracy'] * 100:.2f}%")
        m_c2.metric("Test Precision", f"{metrics['test_precision'] * 100:.2f}%")
        m_c3.metric("Test Recall", f"{metrics['test_recall'] * 100:.2f}%")
        m_c4.metric("Test F1-Score", f"{metrics['test_f1_score'] * 100:.2f}%")

        st.markdown("---")
        ev_col1, ev_col2 = st.columns([1, 1])

        with ev_col1:
            st.markdown("#### Held-Out Confusion Matrix")
            if os.path.exists(cm_img_file):
                st.image(cm_img_file, use_container_width=True)
            else:
                cm = metrics["confusion_matrix"]
                st.write(cm)

            st.caption(
                f"Evaluated on {metrics['test_samples']} test samples (20% stratified split of {metrics['dataset_size_total']} total samples)."
            )

        with ev_col2:
            st.markdown("#### Random Forest Feature Importances")
            importances = metrics.get("feature_importances", {})
            if importances:
                fi_df = pd.DataFrame({
                    "Feature": list(importances.keys()),
                    "Importance": list(importances.values())
                }).sort_values(by="Importance", ascending=True)

                fig_fi = px.bar(
                    fi_df, x="Importance", y="Feature", orientation="h",
                    color="Importance",
                    color_continuous_scale="Viridis",
                    title="Feature Contribution to Irrigation Decision"
                )
                fig_fi.update_layout(template="plotly_dark", height=320, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig_fi, use_container_width=True)

        st.markdown("""
        <div class="honesty-box">
            <b>🔬 Scientific Honesty Notice:</b><br>
            The dataset evaluated is a reproducible synthetic simulation (seed=42) generated with agronomic rules.
            The high test accuracy (88.2%) validates that the Random Forest model successfully learned the mathematical
            evapotranspiration and soil deficit boundaries. It does <b>not</b> guarantee equivalent accuracy in uncalibrated
            real-world agricultural soils with varying crop root depth or soil texture types.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Evaluation metrics file not found. Please run 'python train_model.py'.")


# ==========================================
# TAB 4: PREDICTION HISTORY & TRENDS
# ==========================================
with tab_history:
    st.markdown("### 📈 Edge Telemetry History & Time-Series Trends")

    history_df = engine.get_history_df(limit=150)

    if not history_df.empty:
        # Action summary counters
        total_events = len(history_df)
        valve_open_count = len(history_df[history_df["action_code"] == "VALVE_OPEN"])
        valve_closed_count = total_events - valve_open_count

        h_c1, h_c2, h_c3, h_c4 = st.columns(4)
        h_c1.metric("Total Edge Events Logged", total_events)
        h_c2.metric("Irrigation Cycles (Valve Open)", valve_open_count)
        h_c3.metric("Water Conserved (Valve Closed)", valve_closed_count)
        avg_latency = history_df["latency_ms"].mean()
        h_c4.metric("Mean Edge Latency", f"{avg_latency:.2f} ms")

        st.markdown("---")
        st.markdown("#### Soil Moisture & Environmental Sensor Trends")

        # Time-series chart
        history_df["timestamp_dt"] = pd.to_datetime(history_df["timestamp"])
        df_sorted = history_df.sort_values(by="id", ascending=True)

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=df_sorted["timestamp"], y=df_sorted["soil_moisture"],
            name="Soil Moisture (%)", line=dict(color="#10b981", width=3)
        ))
        fig_trend.add_trace(go.Scatter(
            x=df_sorted["timestamp"], y=df_sorted["temperature"],
            name="Temperature (°C)", line=dict(color="#ef4444", width=2, dash="dash")
        ))
        fig_trend.add_trace(go.Scatter(
            x=df_sorted["timestamp"], y=df_sorted["humidity"],
            name="Humidity (%)", line=dict(color="#3b82f6", width=2, dash="dot")
        ))
        # Add critical threshold line
        fig_trend.add_hline(y=20.0, line_dash="dash", line_color="#f59e0b",
                            annotation_text="Critical Moisture Deficit Threshold (20%)",
                            annotation_position="bottom right")

        fig_trend.update_layout(
            template="plotly_dark",
            height=380,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        st.markdown("#### Recent Edge Telemetry Log Table")
        st.dataframe(
            history_df[[
                "id", "timestamp", "soil_moisture", "temperature", "humidity", "rainfall",
                "prediction", "action_code", "irrigation_probability", "latency_ms"
            ]],
            use_container_width=True,
            height=250
        )

        col_csv, col_clear = st.columns([1, 1])
        csv_data = history_df.to_csv(index=False).encode("utf-8")
        col_csv.download_button(
            label="📥 Download Telemetry Log (CSV)",
            data=csv_data,
            file_name=f"edge_telemetry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        if col_clear.button("🗑️ Clear Telemetry Database", use_container_width=True):
            engine.clear_history()
            st.rerun()
    else:
        st.info("No telemetry recorded yet. Go to the 'Live IoT Simulation' tab and generate readings!")


# ==========================================
# TAB 5: AZURE ML & EDGE LIFECYCLE
# ==========================================
with tab_azure:
    st.markdown("### ☁️ Azure Machine Learning & Edge Deployment Lifecycle")

    az_status = check_azure_status()

    az_col1, az_col2 = st.columns([1.2, 1])

    with az_col1:
        st.markdown("#### Current Cloud Integration Status")

        receipt = az_status.get("last_receipt")
        if receipt and receipt.get("success"):
            st.success(f"✅ **Azure ML Registration Active**\n\n"
                       f"- Model Name: `{receipt.get('model_name')}`\n"
                       f"- Model Version: `{receipt.get('model_version')}`\n"
                       f"- Workspace: `{receipt.get('workspace')}`")
        else:
            st.warning("⚠️ **Azure ML Registration: Standby / Unconfigured**")
            st.markdown("""
            The local application is operating in **Autonomous Edge Mode**.
            Cloud credentials were not detected in the current runtime environment.
            This is normal for offline/edge operation.
            """)

        st.markdown("##### Configuration Diagnostics:")
        diag_df = pd.DataFrame({
            "Parameter": ["Subscription ID", "Resource Group", "Workspace Name", "Local Model File"],
            "Status": [
                az_status["subscription_id"],
                az_status["resource_group"],
                az_status["workspace_name"],
                "Found (models/irrigation_model.joblib)" if az_status["model_file_exists"] else "Missing"
            ]
        })
        st.table(diag_df)

    with az_col2:
        st.markdown("#### 🛠️ How to Connect Azure ML Workspace")
        st.code("""
# 1. Authenticate with Azure CLI
az login

# 2. Export Workspace Configuration (PowerShell)
$env:AZURE_SUBSCRIPTION_ID="your-subscription-id"
$env:AZURE_RESOURCE_GROUP="your-resource-group"
$env:AZURE_WORKSPACE_NAME="your-workspace-name"

# 3. Execute Model Registration Script
python register_azure_model.py
        """, language="powershell")

    st.markdown("---")
    st.markdown("#### 🏭 Real-World IoT Edge Deployment Architecture (Theoretical Rationale)")
    st.markdown("""
    In a physical industrial agricultural deployment:
    1. **Azure Machine Learning** serves as the central MLOps control plane for training on aggregated telemetry across seasons.
    2. Once validated, Azure ML registers the containerized model asset and pushes it to an **Azure Container Registry (ACR)**.
    3. **Azure IoT Edge runtime (iotedged)** running on an in-field gateway (e.g., Raspberry Pi 4 or Advantech industrial gateway) pulls the container image.
    4. Sensor nodes communicate locally over **LoRaWAN or Zigbee** to the edge gateway.
    5. The edge gateway performs **zero-latency offline inference**, directly driving relay switches to solenoid irrigation valves.
    """)
    st.markdown("""
    <div class="honesty-box">
        <b>⚠️ Reality Check:</b><br>
        The demonstration running on this machine is an <b>Edge-Style Local Simulation</b>.
        No physical LoRaWAN sensors or real Azure IoT Edge runtime daemon have been deployed.
        All telemetry is locally simulated and processed via in-process Python runtime.
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6b7280; font-size: 0.8rem;'>"
    "PBA-2 Real-Time ML Application • Smart Agriculture IoT Edge • Practical Exam Build 2026"
    "</div>",
    unsafe_allow_html=True
)
