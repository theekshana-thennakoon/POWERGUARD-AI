import os
import glob
import re
import time
import base64
import warnings
from collections import Counter
import numpy as np
import pandas as pd
import streamlit as st
import joblib

# Suppress minor version warning from scikit-learn
warnings.filterwarnings("ignore")

# ---------------------------------------------------------
# Page Configuration & Industrial Modern Styling
# ---------------------------------------------------------
LOGO_PATH = "Logo.PNG"

st.set_page_config(
    page_title="PowerGuard AI | Next-Gen Electrical Diagnostics",
    page_icon=LOGO_PATH if os.path.exists(LOGO_PATH) else "⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Cyber-Industrial Aesthetics with Skeleton Shimmer Loaders
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    code, pre {
        font-family: 'JetBrains Mono', monospace;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Completely Remove Deploy Option & Clean Header Toolbar */
    [data-testid="stDeployButton"],
    .stDeployButton,
    button[title="Deploy this app"],
    [data-testid="stAppDeployButton"],
    div[data-testid="stToolbar"] > div:first-child:not(:last-child),
    header [data-testid="stToolbar"] > span:first-child,
    header [data-testid="stToolbar"] button:first-child:not(:last-child) {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    /* Shimmer Skeleton Loaders */
    @keyframes skeleton-shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    .skeleton-box {
        background: linear-gradient(90deg, rgba(30, 41, 59, 0.7) 25%, rgba(56, 189, 248, 0.22) 50%, rgba(30, 41, 59, 0.7) 75%);
        background-size: 200% 100%;
        animation: skeleton-shimmer 1.4s infinite ease-in-out;
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.15);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    .skeleton-kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 22px;
    }
    .skeleton-kpi-card {
        height: 120px;
    }
    .skeleton-banner {
        height: 75px;
        margin-bottom: 22px;
    }
    .skeleton-advice-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin-bottom: 22px;
    }
    .skeleton-advice-card {
        height: 95px;
    }
    .skeleton-chart-container {
        height: 310px;
        margin-top: 16px;
        margin-bottom: 22px;
    }
    .skeleton-table {
        height: 240px;
        margin-bottom: 22px;
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 50%, rgba(14, 116, 144, 0.3) 100%);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 16px;
        padding: 22px 28px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px -10px rgba(2, 132, 199, 0.3);
        backdrop-filter: blur(12px);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.15) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8 0%, #a5b4fc 50%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .hero-sub {
        color: #94a3b8;
        font-size: 0.95rem;
        margin: 4px 0 0 0;
        font-weight: 400;
    }
    .hero-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(14, 165, 233, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 8px;
    }

    /* Modern Glassmorphic Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 14px;
        padding: 20px 22px;
        box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, border-color 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .metric-card:hover {
        border-color: rgba(56, 189, 248, 0.4);
        transform: translateY(-2px);
    }
    .metric-card h4 {
        color: #94a3b8;
        font-size: 0.8rem;
        margin: 0 0 8px 0;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .metric-card .value {
        color: #f8fafc;
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        line-height: 1.1;
    }
    .metric-card .subtext {
        color: #38bdf8;
        font-size: 0.85rem;
        margin-top: 8px;
        font-weight: 500;
    }

    /* Pulse Indicator */
    .pulse-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px currentColor;
        animation: pulse-glow 2s infinite ease-in-out;
    }
    @keyframes pulse-glow {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.3); opacity: 0.7; }
    }

    /* Status Badges */
    .status-badge-green {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(21, 128, 61, 0.25) 100%);
        color: #4ade80;
        border: 1px solid rgba(74, 222, 128, 0.4);
        padding: 8px 18px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 1.15rem;
        box-shadow: 0 0 16px rgba(34, 197, 94, 0.2);
    }
    .status-badge-yellow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, rgba(234, 179, 8, 0.15) 0%, rgba(161, 98, 7, 0.25) 100%);
        color: #fde047;
        border: 1px solid rgba(250, 204, 21, 0.4);
        padding: 8px 18px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 1.15rem;
        box-shadow: 0 0 16px rgba(234, 179, 8, 0.2);
    }
    .status-badge-red {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(185, 28, 28, 0.25) 100%);
        color: #f87171;
        border: 1px solid rgba(248, 113, 113, 0.4);
        padding: 8px 18px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 1.15rem;
        box-shadow: 0 0 16px rgba(239, 68, 68, 0.25);
    }

    /* Device Pills */
    .device-pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: #ffffff;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 6px;
        margin-top: 4px;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }

    /* Diagnostic Advice Box */
    .advice-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%);
        border-left: 4px solid #38bdf8;
        border-top: 1px solid rgba(148, 163, 184, 0.1);
        border-right: 1px solid rgba(148, 163, 184, 0.1);
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        padding: 16px 20px;
        border-radius: 0 12px 12px 0;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    .advice-card strong {
        color: #38bdf8;
        font-size: 1.0rem;
    }
    .advice-card p {
        color: #cbd5e1;
        margin: 6px 0 0 0;
        font-size: 0.9rem;
        line-height: 1.45;
    }

    /* Section divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.3), transparent);
        margin: 24px 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Logo Base64 Loader & Snippets
# ---------------------------------------------------------
@st.cache_data
def get_logo_base64():
    """Reads Logo.PNG and converts it into a base64 Data URI."""
    if os.path.exists(LOGO_PATH):
        try:
            with open(LOGO_PATH, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
                return f"data:image/png;base64,{encoded}"
        except Exception:
            return None
    return None

logo_b64 = get_logo_base64()

# Small Logo HTML Elements
sidebar_logo_tag = f'<img src="{logo_b64}" alt="Logo" style="width: 40px; height: 40px; object-fit: contain; border-radius: 8px; background: rgba(255,255,255,0.06); padding: 3px; border: 1px solid rgba(56, 189, 248, 0.25); box-shadow: 0 0 10px rgba(56, 189, 248, 0.15);">' if logo_b64 else '<span style="font-size: 2.0rem;">⚡</span>'
hero_logo_tag = f'<img src="{logo_b64}" alt="Logo" style="width: 48px; height: 48px; object-fit: contain; border-radius: 10px; background: rgba(255,255,255,0.06); padding: 4px; border: 1px solid rgba(56, 189, 248, 0.3); box-shadow: 0 0 14px rgba(56, 189, 248, 0.2);">' if logo_b64 else ''

# ---------------------------------------------------------
# Constants & Model Loading
# ---------------------------------------------------------
DATA_DIR = "data"
HISTORY_FILE = os.path.join(DATA_DIR, "history.csv")
MODEL_FILE = "device_model.pkl"
BASELINE_FILE = os.path.join(DATA_DIR, "baseline_stats.csv")

feature_cols = [
    "U1_rms_AVG", "I1_rms_AVG", "U2_rms_AVG", "I2_rms_AVG", "U3_rms_AVG", "I3_rms_AVG",
    "Freq_AVG", "P_sum_AVG", "PF_sum_AVG",
    "U1_thd-f_AVG", "U2_thd-f_AVG", "U3_thd-f_AVG",
    "U1_H5_AVG", "U1_H7_AVG", "U2_H5_AVG", "U2_H7_AVG", "U3_H5_AVG", "U3_H7_AVG",
    "I1_H5_AVG", "I1_H7_AVG", "I2_H5_AVG", "I2_H7_AVG", "I3_H5_AVG", "I3_H7_AVG",
]

# Identification features (intrinsic device signatures)
id_cols = ["I1_rms_AVG", "I2_rms_AVG", "I3_rms_AVG", "P_sum_AVG", "PF_sum_AVG"]

# Tolerance thresholds: (yellow limit, red limit)
LIMITS = {
    "Current": (0.05, 0.15),
    "Power": (0.05, 0.15),
    "Power Factor": (0.05, 0.10),
    "Harmonic": (0.20, 0.50),
    "Voltage": (0.03, 0.08),
    "Frequency": (0.005, 0.01),
}

# Absolute change thresholds (prevents noise flags on low idle lines)
MIN_CHANGE = {
    "Current": 0.05,
    "Power": 20,
    "Power Factor": 0.03,
    "Harmonic": 0,
    "Voltage": 0,
    "Frequency": 0
}

DEVICE_CATEGORIES = ["Current", "Power", "Power Factor"]

# Health Status evaluation criteria
MIN_RUN = 3           # minimum consecutive readings to count sustained fault (15 s)
YELLOW_SHARE = 0.05   # >= 5% sustained flagged readings -> YELLOW
RED_SHARE = 0.20      # >= 20% sustained flagged readings -> RED
RED_ROWS_SHARE = 0.10 # >= 10% severe red readings -> RED

ADVICE = {
    ("Current", "up"): "Current is higher than normal. Check for mechanical overload, worn/seized bearings, blocked cooling fans, or jammed motor rotor.",
    ("Current", "down"): "Current is lower than normal. Inspect for disconnected phases, loose terminal lugs, open coils, or lost mechanical load.",
    ("Power", "up"): "Power consumption is elevated. Check for heavy mechanical friction, uncalibrated load, or abnormal thermal dissipation.",
    ("Power", "down"): "Power draw has decreased. Verify device operating state, loss of driven load, or power supply degradation.",
    ("Power Factor", "down"): "Power factor has dropped significantly. Inspect motor stator windings, check power factor correction capacitors, or check for light idle loading.",
    ("Power Factor", "up"): "Power factor is higher than typical baseline. Confirm whether capacitive loads or different operational profiles are active.",
    ("Harmonic", "up"): "Harmonics (THD / H5 / H7) are elevated. Inspect for failing inverter rectifiers, non-linear switching noise, or defective EMI filters.",
    ("Voltage", "down"): "Line voltage is depressed. Potential heavy facility load draw, loose upstream transformer tap, or utility voltage sag.",
}

# ---------------------------------------------------------
# Skeleton HTML Generators
# ---------------------------------------------------------
def render_skeleton_kpis():
    """Generates skeleton placeholder HTML for the 4 metric cards."""
    return """
    <div class="skeleton-kpi-grid">
        <div class="skeleton-box skeleton-kpi-card"></div>
        <div class="skeleton-box skeleton-kpi-card"></div>
        <div class="skeleton-box skeleton-kpi-card"></div>
        <div class="skeleton-box skeleton-kpi-card"></div>
    </div>
    """

def render_skeleton_banner():
    """Generates skeleton placeholder HTML for operational assessment."""
    return '<div class="skeleton-box skeleton-banner"></div>'

def render_skeleton_advice():
    """Generates skeleton placeholder HTML for diagnostic advice cards."""
    return """
    <div class="skeleton-advice-grid">
        <div class="skeleton-box skeleton-advice-card"></div>
        <div class="skeleton-box skeleton-advice-card"></div>
        <div class="skeleton-box skeleton-advice-card"></div>
    </div>
    """

def render_skeleton_chart():
    """Generates skeleton placeholder HTML for waveform chart tabs."""
    return '<div class="skeleton-box skeleton-chart-container"></div>'

def render_skeleton_table():
    """Generates skeleton placeholder HTML for data tables."""
    return '<div class="skeleton-box skeleton-table"></div>'

# ---------------------------------------------------------
# Background Asset Loader (No Raw Function Spinner)
# ---------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_system_assets():
    """Load pre-trained model and baseline statistics silently without blocking raw spinners."""
    model = None
    baseline_stats = None
    if os.path.exists(MODEL_FILE):
        model = joblib.load(MODEL_FILE)
    if os.path.exists(BASELINE_FILE):
        baseline_stats = pd.read_csv(BASELINE_FILE, header=[0, 1], index_col=0)
    return model, baseline_stats

model, baseline_stats = load_system_assets()

def categorize_feature(f):
    if "thd" in f or "H5" in f or "H7" in f:
        return "Harmonic"
    if f.startswith("PF"):
        return "Power Factor"
    if f.startswith("P"):
        return "Power"
    if f.startswith("I"):
        return "Current"
    if f.startswith("U"):
        return "Voltage"
    if f.startswith("Freq"):
        return "Frequency"
    return "Other"

def check_deviation(reading, device, z_threshold=3):
    """Flag a feature only if it is unusual (z-score) AND exceeds relative & absolute limits."""
    alerts = []
    if baseline_stats is None or device not in baseline_stats.index:
        return alerts

    for f in feature_cols:
        try:
            mean = baseline_stats.loc[device, (f, "mean")]
            std = baseline_stats.loc[device, (f, "std")]
        except KeyError:
            continue

        value = reading[f]
        cat = categorize_feature(f)
        if cat == "Power Factor":
            value, mean = abs(value), abs(mean)
        if std == 0 or pd.isna(std):
            continue

        z = (value - mean) / std
        change = abs(value - mean)
        rel = change / abs(mean) if mean != 0 else 0
        yellow, red = LIMITS.get(cat, (0.05, 0.15))
        min_c = MIN_CHANGE.get(cat, 0)

        if abs(z) > z_threshold and rel > yellow and change > min_c:
            alerts.append({
                "feature": f,
                "category": cat,
                "value": round(float(value), 3),
                "expected": round(float(mean), 3),
                "z": round(float(z), 2),
                "percent": round(rel * 100, 1),
                "direction": "up" if value > mean else "down",
                "level": "red" if rel > red else "yellow",
            })
    return alerts

def summarize_recording(df, device, file_name):
    """Compute recording summary and health metrics for history logging."""
    body = df.iloc[8:] if len(df) > 8 else df
    
    if "Date" in df.columns and "Time" in df.columns:
        recorded_at = pd.to_datetime(df["Date"].astype(str) + " " + df["Time"].astype(str), errors="coerce").iloc[0]
        if pd.isna(recorded_at):
            recorded_at = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        recorded_at = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

    z_list = []
    if baseline_stats is not None and device in baseline_stats.index:
        for f in feature_cols:
            try:
                mean = baseline_stats.loc[device, (f, "mean")]
                std = baseline_stats.loc[device, (f, "std")]
                if std > 0 and not pd.isna(std):
                    z_list.append(abs((body[f].mean() - mean) / std))
            except KeyError:
                continue

    return {
        "recorded_at": str(recorded_at),
        "saved_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file_name": file_name,
        "device": device,
        "readings": len(body),
        "current_A": round(body[["I1_rms_AVG", "I2_rms_AVG", "I3_rms_AVG"]].mean().sum(), 4),
        "power_W": round(body["P_sum_AVG"].mean(), 2),
        "power_factor": round(abs(body["PF_sum_AVG"].mean()), 4),
        "voltage_thd": round(body[["U1_thd-f_AVG", "U2_thd-f_AVG", "U3_thd-f_AVG"]].mean().mean(), 4),
        "current_H5": round(body[["I1_H5_AVG", "I2_H5_AVG", "I3_H5_AVG"]].mean().sum(), 4),
        "current_H7": round(body[["I1_H7_AVG", "I2_H7_AVG", "I3_H7_AVG"]].mean().sum(), 4),
        "health_score": round(float(np.mean(z_list)) if z_list else 0.0, 3),
    }

def save_to_history(summary):
    """Save an inspection summary row to history.csv preventing duplicates."""
    new_row = pd.DataFrame([summary])
    if os.path.exists(HISTORY_FILE):
        old = pd.read_csv(HISTORY_FILE)
        dup = ((old["file_name"] == summary["file_name"]) &
               (old["device"] == summary["device"]) &
               (old["recorded_at"].astype(str) == str(summary["recorded_at"]))).any()
        if dup:
            return False
        combined = pd.concat([old, new_row], ignore_index=True)
    else:
        combined = new_row
    os.makedirs(DATA_DIR, exist_ok=True)
    combined.to_csv(HISTORY_FILE, index=False)
    return True

def analyze_dataset(df, device_override=None):
    """Run full stage 1 (Identification) and stage 2 (Health Detection) on a dataframe."""
    predictions = model.predict(df[id_cols])
    df["Predicted_Device"] = predictions
    predicted_device = pd.Series(predictions).mode()[0]
    confidence = (predictions == predicted_device).mean()

    device = device_override if device_override else predicted_device

    # Skip first 8 rows (initial startup transients)
    check_df = df.iloc[8:] if len(df) > 8 else df

    flagged, info_rows = [], []
    for pos, (idx, row) in enumerate(check_df.iterrows()):
        alerts = check_deviation(row, device)
        if not (len(alerts) >= 2 or any(abs(a["z"]) > 5 for a in alerts)):
            continue
        dev_alerts = [a for a in alerts if a["category"] in DEVICE_CATEGORIES]
        if dev_alerts:
            level = "red" if any(a["level"] == "red" for a in dev_alerts) else "yellow"
            flagged.append((pos, idx, level, alerts))
        else:
            info_rows.append((idx, alerts))

    # Identify sustained runs of MIN_RUN or more
    keep, run = set(), []
    for p in [f[0] for f in flagged] + [None]:
        if run and (p is None or p != run[-1] + 1):
            if len(run) >= MIN_RUN:
                keep.update(run)
            run = []
        if p is not None:
            run.append(p)

    all_rows = [(idx, lvl, al) for pos, idx, lvl, al in flagged]
    fault_rows = [(idx, lvl, al) for pos, idx, lvl, al in flagged if pos in keep]
    n_isolated = len(all_rows) - len(fault_rows)

    n_checked = max(len(check_df), 1)
    flagged_fraction = len(all_rows) / n_checked
    fault_fraction = len(fault_rows) / n_checked
    red_rows = sum(1 for _, lvl, _ in fault_rows if lvl == "red")
    red_fraction = red_rows / n_checked
    health_pct = max(0, round(100 * (1 - flagged_fraction)))

    if fault_fraction >= RED_SHARE or red_fraction >= RED_ROWS_SHARE:
        status = "RED"
    elif fault_fraction >= YELLOW_SHARE:
        status = "YELLOW"
    else:
        status = "GREEN"

    return {
        "predictions": predictions,
        "predicted_device": predicted_device,
        "active_device": device,
        "confidence": confidence,
        "check_df": check_df,
        "all_rows": all_rows,
        "fault_rows": fault_rows,
        "n_isolated": n_isolated,
        "n_checked": n_checked,
        "health_pct": health_pct,
        "status": status,
        "info_rows": info_rows,
    }


# ---------------------------------------------------------
# Sidebar Navigation & System Telemetry with Small Logo
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
        {sidebar_logo_tag}
        <div>
            <h3 style="margin: 0; font-size: 1.25rem; font-weight: 800; color: #f8fafc; letter-spacing: -0.02em;">POWERGUARD</h3>
            <span style="font-size: 0.72rem; color: #38bdf8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em;">AI HEALTH ENGINE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    menu = st.radio(
        "NAVIGATION MENU",
        [
            "⚡ Live Inspection & Diagnostics",
            "🧪 Fault Injection Simulator",
            "📈 Fleet History & Degradation Trends",
            "📋 Device Baseline Catalog",
            "🧠 System Architecture & Methodology",
        ],
        index=0
    )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("#### System Telemetry")
    
    if model is not None:
        st.markdown("""
        <div style="background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 8px; padding: 10px 14px; margin-bottom: 8px;">
            <span class="pulse-dot" style="color: #22c55e; margin-right: 6px;"></span>
            <strong style="color: #4ade80; font-size: 0.85rem;">Classifier Online</strong><br>
            <span style="color: #94a3b8; font-size: 0.75rem;">25 Active Load Profiles</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Classifier Offline (device_model.pkl)")

    if baseline_stats is not None:
        st.markdown(f"""
        <div style="background: rgba(14, 165, 233, 0.1); border: 1px solid rgba(14, 165, 233, 0.3); border-radius: 8px; padding: 10px 14px; margin-bottom: 8px;">
            <strong style="color: #38bdf8; font-size: 0.85rem;">Baseline Calibrated</strong><br>
            <span style="color: #94a3b8; font-size: 0.75rem;">{len(baseline_stats.index)} Statistical Profiles</span>
        </div>
        """, unsafe_allow_html=True)

    hist_count = len(pd.read_csv(HISTORY_FILE)) if os.path.exists(HISTORY_FILE) else 0
    st.caption(f"📁 History Records: **{hist_count} inspections**")


# ==============================================================================
# VIEW 1: LIVE INSPECTION & DIAGNOSTICS
# ==============================================================================
if menu == "⚡ Live Inspection & Diagnostics":
    # Top Hero Banner with Small Integrated Logo
    st.markdown(f"""
    <div class="hero-banner">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
            <div style="display: flex; align-items: center; gap: 16px;">
                {hero_logo_tag}
                <div>
                    <h1 class="hero-title">POWERGUARD AI</h1>
                    <p class="hero-sub">Industrial Device Identification & Sub-second Early Fault Detection Platform</p>
                    <div class="hero-tag">
                        <span class="pulse-dot" style="color: #38bdf8;"></span>
                        3-Phase Electrical Signature Diagnostics
                    </div>
                </div>
            </div>
            <div style="text-align: right;">
                <span class="status-badge-green" style="font-size: 0.85rem; padding: 6px 14px;">
                    <span class="pulse-dot" style="color: #4ade80;"></span> LIVE TELEMETRY
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Data Source Selection (Upload vs Curated Sample)
    st.markdown("#### Select Inspection Source")
    source_choice = st.radio(
        "Data Source Selection:",
        ["📂 Select Pre-loaded Lab Sample", "📁 Upload CSV Recording"],
        horizontal=True,
        label_visibility="collapsed"
    )

    df_loaded = None
    file_name = None

    if source_choice == "📁 Upload CSV Recording":
        uploaded_file = st.file_uploader(
            "Upload Power Analyzer CSV file",
            type=["csv"],
            help="File must contain 3-phase RMS voltages, currents, active power, power factor, and harmonics."
        )
        if uploaded_file is not None:
            try:
                df_loaded = pd.read_csv(uploaded_file)
                file_name = uploaded_file.name
            except Exception as e:
                st.error(f"Error reading uploaded CSV: {e}")
    else:
        # Discover all CSVs in data/
        available_files = [os.path.basename(p) for p in glob.glob(os.path.join(DATA_DIR, "*.csv"))
                           if not os.path.basename(p).startswith("combined_")
                           and not os.path.basename(p).startswith("baseline_")
                           and not os.path.basename(p).startswith("history")]
        
        curated_defaults = [
            "D8_3PhaseMotor_solo.csv",
            "D9_1PhaseMotor_solo.csv",
            "D11_AC_solo.csv",
            "D1_Light_solo_s4.csv",
            "D4_Laptop_solo_s2.csv",
            "D5_UPS_solo_s3.csv",
            "D10_Transformer_solo.csv",
            "P01_LED_UPS_s4.csv",
            "P03_LED_Laptop_s3.csv",
            "P08_1PhaseMotor_LED.csv",
            "P13_UPS_AC_s2.csv",
            "Random single phase Motor.csv",
            "Random single phase Motor 2.csv",
        ]
        options = [f for f in curated_defaults if f in available_files] + [f for f in available_files if f not in curated_defaults]

        col_select, col_info = st.columns([2, 1])
        with col_select:
            selected_sample = st.selectbox(
                "Choose pre-recorded electrical recording:",
                options,
                index=0
            )
        with col_info:
            st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 10px; padding: 10px 14px; margin-top: 5px;">
                <span style="color: #38bdf8; font-size: 0.8rem; font-weight: 600;">INSTANT READY</span><br>
                <span style="color: #cbd5e1; font-size: 0.78rem;">Loaded with clean steady-state lab sessions & combination loads.</span>
            </div>
            """, unsafe_allow_html=True)

        if selected_sample:
            sample_path = os.path.join(DATA_DIR, selected_sample)
            if os.path.exists(sample_path):
                df_loaded = pd.read_csv(sample_path)
                file_name = selected_sample

    # Skeleton placeholder container
    main_placeholder = st.empty()

    if df_loaded is not None:
        missing = [c for c in feature_cols if c not in df_loaded.columns]
        if missing:
            st.error(f"⚠️ Missing {len(missing)} required electrical channels: {missing}")
            st.info("The recording must contain 3-phase RMS voltages, currents, active power, power factor, and harmonics.")
        else:
            # Display Animated Shimmer Skeleton Loader While Preparing Analysis
            main_placeholder.markdown(
                f"""
                <div class="custom-divider"></div>
                {render_skeleton_kpis()}
                {render_skeleton_banner()}
                {render_skeleton_chart()}
                """,
                unsafe_allow_html=True
            )
            
            # Smooth loading transition
            time.sleep(0.35)

            # Run Actual System Analysis
            analysis = analyze_dataset(df_loaded)
            device = analysis["predicted_device"]
            status = analysis["status"]
            confidence = analysis["confidence"]
            health_pct = analysis["health_pct"]
            all_rows = analysis["all_rows"]
            fault_rows = analysis["fault_rows"]
            n_checked = analysis["n_checked"]
            info_rows = analysis["info_rows"]
            summary = summarize_recording(df_loaded, device, file_name)

            # Clear skeleton and render the real content
            with main_placeholder.container():
                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                
                # --- Top KPI Summary Cards ---
                kpi1, kpi2, kpi3, kpi4 = st.columns(4)
                with kpi1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4><span>🏷️</span> Identified Equipment</h4>
                        <p class="value">{device}</p>
                        <div class="subtext">AI Classification: {confidence:.1%} Agreement</div>
                    </div>
                    """, unsafe_allow_html=True)

                with kpi2:
                    if status == "GREEN":
                        badge_html = '<span class="status-badge-green"><span class="pulse-dot" style="color: #4ade80;"></span> HEALTHY</span>'
                        sub = f"All {n_checked} readings within tolerance"
                    elif status == "YELLOW":
                        badge_html = '<span class="status-badge-yellow"><span class="pulse-dot" style="color: #facc15;"></span> WARNING</span>'
                        sub = f"{len(fault_rows)} sustained deviations detected"
                    else:
                        badge_html = '<span class="status-badge-red"><span class="pulse-dot" style="color: #f87171;"></span> CRITICAL FAULT</span>'
                        sub = f"{len(fault_rows)} severe deviations detected"

                    st.markdown(f"""
                    <div class="metric-card">
                        <h4><span>🚨</span> Diagnostic Health Status</h4>
                        <div style="margin-top: 4px; margin-bottom: 4px;">{badge_html}</div>
                        <div class="subtext">{sub}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with kpi3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4><span>📈</span> Operational Health Index</h4>
                        <p class="value">{health_pct}%</p>
                        <div class="subtext">Baseline Z-Score: {summary['health_score']:.2f} (lower is better)</div>
                    </div>
                    """, unsafe_allow_html=True)

                with kpi4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4><span>⚡</span> Active Power & Load</h4>
                        <p class="value">{summary['power_W']} W</p>
                        <div class="subtext">Current: {summary['current_A']} A &bull; PF: {summary['power_factor']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Sub-components pill tags if combination device
                if "+" in device:
                    st.markdown("<div style='margin-top: 14px;'>", unsafe_allow_html=True)
                    st.write("**Active Composite Sub-Loads Detected:**")
                    components = device.split("+")
                    pills = " ".join([f'<span class="device-pill">⚡ {c.strip()}</span>' for c in components])
                    st.markdown(pills, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                # --- Status Assessment Banner ---
                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                st.markdown("### Operational Diagnostic Assessment")
                
                if status == "GREEN":
                    st.success(f"🟢 **Optimal Health:** The connected equipment **{device}** is operating within calibrated nominal electrical baselines. No sustained abnormalities detected.")
                elif status == "YELLOW":
                    st.warning(f"🟡 **Minor Deviation Notice:** **{device}** demonstrates early operational variations ({len(fault_rows)} readings flagged). Recommended for scheduled preventative maintenance check.")
                else:
                    st.error(f"🔴 **Immediate Inspection Alert:** **{device}** exhibits severe electrical deviations exceeding safe tolerance thresholds. Immediate inspection required.")

                if analysis["n_isolated"] > 0:
                    st.caption(f"ℹ️ Note: {analysis['n_isolated']} isolated electrical spikes were detected (< {MIN_RUN} consecutive cycles) and automatically filtered out to prevent false alarms.")

                # --- Grid vs Device Event Detection ---
                if info_rows:
                    st.info(f"⚡ **External Supply/Grid Disturbance Detected:** {len(info_rows)} reading(s) registered line voltage/harmonic fluctuations without a corresponding device current anomaly. This reflects upstream utility grid variations rather than an internal machine fault.")

                # --- Maintenance Advice & Root Causes ---
                if all_rows:
                    st.markdown("### 🛠️ Root-Cause Diagnostics & Actionable Advice")
                    counts = Counter()
                    for _, _, alerts in all_rows:
                        for a in alerts:
                            if a["category"] in DEVICE_CATEGORIES:
                                counts[(a["category"], a["direction"])] += 1

                    if counts:
                        advice_cols = st.columns(min(len(counts), 3))
                        col_idx = 0
                        for (cat, direction), n in counts.most_common(3):
                            with advice_cols[col_idx % 3]:
                                action_text = ADVICE.get((cat, direction), "Inspect the machine and verify against baseline parameters.")
                                st.markdown(f"""
                                <div class="advice-card">
                                    <strong>{cat} {'Surge ▲' if direction == 'up' else 'Drop ▼'} ({n} events)</strong>
                                    <p>{action_text}</p>
                                </div>
                                """, unsafe_allow_html=True)
                            col_idx += 1

                # --- Interactive Electrical Signals & Curves (All Tabs) ---
                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                st.subheader("📊 Electrical Parameter Profiles & Waveform Trajectories")
                tab_current, tab_power, tab_volt, tab_harm, tab_predictions = st.tabs([
                    "⚡ Phase Currents (I1, I2, I3)",
                    "🔌 Power & Power Factor",
                    "📈 Voltages (U1, U2, U3)",
                    "〰️ Harmonics (THD & H5/H7)",
                    "🎯 AI Prediction Distribution"
                ])

                with tab_current:
                    st.caption("3-Phase RMS Currents (Amperes) across recording duration")
                    chart_df = df_loaded[["I1_rms_AVG", "I2_rms_AVG", "I3_rms_AVG"]].copy()
                    st.line_chart(chart_df, color=["#38bdf8", "#34d399", "#f59e0b"])

                with tab_power:
                    col_p, col_pf = st.columns(2)
                    with col_p:
                        st.caption("Total Active Power P_sum (Watts)")
                        st.line_chart(df_loaded["P_sum_AVG"], color=["#38bdf8"])
                    with col_pf:
                        st.caption("Power Factor PF_sum (0.0 to 1.0)")
                        st.line_chart(df_loaded["PF_sum_AVG"].abs(), color=["#a855f7"])

                with tab_volt:
                    st.caption("3-Phase RMS Voltages (Volts)")
                    st.line_chart(df_loaded[["U1_rms_AVG", "U2_rms_AVG", "U3_rms_AVG"]], color=["#f43f5e", "#0ea5e9", "#10b981"])

                with tab_harm:
                    col_h1, col_h2 = st.columns(2)
                    with col_h1:
                        st.caption("Voltage Total Harmonic Distortion THD (%)")
                        st.line_chart(df_loaded[["U1_thd-f_AVG", "U2_thd-f_AVG", "U3_thd-f_AVG"]], color=["#ec4899", "#8b5cf6", "#06b6d4"])
                    with col_h2:
                        st.caption("Current 5th & 7th Harmonics (A)")
                        st.line_chart(df_loaded[["I1_H5_AVG", "I1_H7_AVG", "I2_H5_AVG", "I2_H7_AVG", "I3_H5_AVG", "I3_H7_AVG"]])

                with tab_predictions:
                    st.caption("AI Classification Breakdown across recording slices")
                    pred_series = pd.Series(analysis["predictions"])
                    st.bar_chart(pred_series.value_counts(), color=["#38bdf8"])

                # --- Flagged Anomalies Inspector ---
                if all_rows:
                    with st.expander(f"🔍 Inspect Flagged Deviations Log ({len(all_rows)} events)"):
                        anomaly_records = []
                        for row_idx, lvl, alerts in all_rows:
                            timestamp = f"{df_loaded['Date'].iloc[row_idx]} {df_loaded['Time'].iloc[row_idx]}" if "Date" in df_loaded.columns else f"Row {row_idx}"
                            for a in alerts:
                                anomaly_records.append({
                                    "Row": row_idx,
                                    "Time": timestamp,
                                    "Severity": lvl.upper(),
                                    "Parameter": a["feature"],
                                    "Category": a["category"],
                                    "Observed": a["value"],
                                    "Nominal": a["expected"],
                                    "Change %": f"{'+' if a['direction']=='up' else '-'}{a['percent']}%",
                                    "Z-Score": a["z"],
                                })
                        anom_df = pd.DataFrame(anomaly_records)
                        st.dataframe(anom_df, use_container_width=True)

                # --- Save to History & Export ---
                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                save_col, export_col = st.columns([1, 1])
                with save_col:
                    if st.button("💾 Save Inspection to Fleet History", type="primary", use_container_width=True):
                        if save_to_history(summary):
                            st.success(f"✓ Successfully registered {file_name} ({device}) in the fleet history database.")
                        else:
                            st.warning("ℹ️ This recording is already registered in the history log.")

                with export_col:
                    csv_data = pd.DataFrame([summary]).to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Diagnostic Summary (CSV)",
                        data=csv_data,
                        file_name=f"diagnostic_report_{device}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )


# ==============================================================================
# VIEW 2: FAULT INJECTION SIMULATOR
# ==============================================================================
elif menu == "🧪 Fault Injection Simulator":
    st.markdown(f"""
    <div class="hero-banner">
        <div style="display: flex; align-items: center; gap: 16px;">
            {hero_logo_tag}
            <div>
                <h1 class="hero-title">FAULT INJECTION SANDBOX</h1>
                <p class="hero-sub">Simulate synthetic electrical & mechanical faults on healthy machinery to validate detection response.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    sim_device = st.selectbox(
        "Select Target Equipment for Simulation:",
        ["1PhaseMotor", "3PhaseMotor", "LED", "Transformer", "AC", "UPS"]
    )

    candidate_files = [f for f in glob.glob(os.path.join(DATA_DIR, "*.csv"))
                       if sim_device.lower() in os.path.basename(f).lower()
                       and "combined" not in f and "baseline" not in f]
    
    if candidate_files:
        base_df = pd.read_csv(candidate_files[0]).copy()
        st.caption(f"Loaded reference recording from: `{os.path.basename(candidate_files[0])}` ({len(base_df)} readings)")
        
        st.markdown("#### Configure Injected Fault Profile")
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            fault_mode = st.selectbox(
                "Simulated Failure Mode:",
                [
                    "Mechanical Bearing Wear / Rotor Jam (Current Surge)",
                    "Capacitor Degradation / Light Loading (Power Factor Drop)",
                    "Supply Under-voltage / Grid Sag (Voltage Drop)",
                    "Non-Linear Inverter Distortion (Harmonic THD Surge)",
                    "Severe Combined Fault (Overload + Degraded PF)",
                ]
            )
        with f_col2:
            severity = st.slider("Fault Severity Magnitude (% deviation):", min_value=10, max_value=100, value=40, step=5)

        # Skeleton placeholder for simulator response
        sim_placeholder = st.empty()
        sim_placeholder.markdown(
            f"""
            <div class="custom-divider"></div>
            {render_skeleton_kpis()}
            {render_skeleton_chart()}
            """,
            unsafe_allow_html=True
        )
        time.sleep(0.3)

        # Apply synthetic degradation to steady-state rows
        modified_df = base_df.copy()
        steady_slice = slice(8, None)

        if "Bearing Wear" in fault_mode:
            multiplier = 1 + (severity / 100.0)
            modified_df.loc[modified_df.index[steady_slice], "I1_rms_AVG"] *= multiplier
            modified_df.loc[modified_df.index[steady_slice], "P_sum_AVG"] *= multiplier
        elif "Capacitor" in fault_mode:
            reduction = 1 - (severity / 100.0 * 0.7)
            modified_df.loc[modified_df.index[steady_slice], "PF_sum_AVG"] *= reduction
        elif "Voltage Drop" in fault_mode:
            reduction = 1 - (severity / 100.0 * 0.25)
            modified_df.loc[modified_df.index[steady_slice], "U1_rms_AVG"] *= reduction
            modified_df.loc[modified_df.index[steady_slice], "U2_rms_AVG"] *= reduction
            modified_df.loc[modified_df.index[steady_slice], "U3_rms_AVG"] *= reduction
        elif "Harmonic" in fault_mode:
            multiplier = 1 + (severity / 100.0 * 3.0)
            modified_df.loc[modified_df.index[steady_slice], "U1_thd-f_AVG"] *= multiplier
            modified_df.loc[modified_df.index[steady_slice], "I1_H5_AVG"] *= multiplier
        elif "Severe Combined" in fault_mode:
            modified_df.loc[modified_df.index[steady_slice], "I1_rms_AVG"] *= (1 + severity / 100.0)
            modified_df.loc[modified_df.index[steady_slice], "PF_sum_AVG"] *= (1 - severity / 100.0 * 0.5)

        # Run Detection Engine on Simulated Stream
        sim_analysis = analyze_dataset(modified_df, device_override=sim_device)
        
        with sim_placeholder.container():
            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
            s_col1, s_col2, s_col3 = st.columns(3)
            with s_col1:
                st.metric("Detection System Status", sim_analysis["status"])
            with s_col2:
                st.metric("Flagged Fault Readings", f"{len(sim_analysis['fault_rows'])} / {sim_analysis['n_checked']}")
            with s_col3:
                st.metric("Degraded Health Score", f"{sim_analysis['health_pct']}%")

            if sim_analysis["status"] == "RED":
                st.error(f"🚨 **Fault Successfully Caught!** The early fault detection engine triggered RED status due to sustained {fault_mode}.")
            elif sim_analysis["status"] == "YELLOW":
                st.warning(f"⚠️ **Early Warning Caught!** The system caught early warning signs (YELLOW status).")
            else:
                st.info("🟢 Deviations remained within nominal tolerance boundaries.")

            # Comparison chart: Healthy vs Injected Signal
            st.markdown("#### Signal Trajectory Under Simulated Stress")
            compare_col = "I1_rms_AVG" if "Bearing" in fault_mode or "Combined" in fault_mode else ("PF_sum_AVG" if "Capacitor" in fault_mode else "U1_rms_AVG")
            comp_df = pd.DataFrame({
                "Original Nominal Signal": base_df[compare_col],
                "Simulated Degraded Signal": modified_df[compare_col]
            })
            st.line_chart(comp_df, color=["#22c55e", "#ef4444"])

    else:
        st.warning(f"No solo test recording found for {sim_device} in {DATA_DIR}.")


# ==============================================================================
# VIEW 3: FLEET HISTORY & DEGRADATION TRENDS
# ==============================================================================
elif menu == "📈 Fleet History & Degradation Trends":
    st.markdown(f"""
    <div class="hero-banner">
        <div style="display: flex; align-items: center; gap: 16px;">
            {hero_logo_tag}
            <div>
                <h1 class="hero-title">FLEET HEALTH & TRENDS</h1>
                <p class="hero-sub">Longitudinal equipment aging curves, multi-session drift monitoring, and predictive warnings.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not os.path.exists(HISTORY_FILE):
        st.warning("No historical inspection logs found. Upload and save recordings in 'Live Inspection' to populate history.")
    else:
        history = pd.read_csv(HISTORY_FILE)
        history["recorded_at"] = pd.to_datetime(history["recorded_at"], errors="coerce")
        history = history.sort_values("recorded_at")

        # Top summary stats with skeleton placeholder
        hist_placeholder = st.empty()
        hist_placeholder.markdown(
            f"""
            {render_skeleton_kpis()}
            {render_skeleton_chart()}
            """,
            unsafe_allow_html=True
        )
        time.sleep(0.3)

        with hist_placeholder.container():
            h1, h2, h3, h4 = st.columns(4)
            with h1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Total Inspections</h4>
                    <p class="value">{len(history)}</p>
                    <div class="subtext">Completed Cycles</div>
                </div>
                """, unsafe_allow_html=True)
            with h2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Monitored Fleet</h4>
                    <p class="value">{history['device'].nunique()}</p>
                    <div class="subtext">Unique Devices</div>
                </div>
                """, unsafe_allow_html=True)
            with h3:
                avg_score = history["health_score"].mean()
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Mean Z-Score</h4>
                    <p class="value">{avg_score:.2f}</p>
                    <div class="subtext">Fleet Health Baseline</div>
                </div>
                """, unsafe_allow_html=True)
            with h4:
                latest_date = history["recorded_at"].max()
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Latest Inspection</h4>
                    <p class="value" style="font-size: 1.4rem;">{str(latest_date)[:10] if pd.notna(latest_date) else 'N/A'}</p>
                    <div class="subtext">Chronological Log</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
            device_options = sorted(history["device"].unique())
            selected_dev = st.selectbox("Select Equipment for Trend Analysis:", device_options)

            dev_hist = history[history["device"] == selected_dev].sort_values("recorded_at")
            st.write(f"Logged inspection cycles for **{selected_dev}**: **{len(dev_hist)}**")

            if len(dev_hist) < 2:
                st.info("💡 At least 2 historical inspections on different dates are required to plot trend curves. Save another recording to view drift curves.")
            else:
                plot_df = dev_hist.set_index("recorded_at")

                # Health Score Drift Curve
                st.markdown("#### Health Score Degradation Trajectory (Z-Score Drift)")
                st.caption("Rising health score indicates progressive deviation away from nominal baseline.")
                st.line_chart(plot_df["health_score"], color=["#f59e0b"])

                # Degradation Drift Alert Engine
                scores = dev_hist["health_score"].tolist()
                if len(scores) >= 3 and scores[-1] > scores[-2] > scores[-3]:
                    st.error("⚠️ **Degradation Trend Alert:** Health score has consecutively worsened over the last 3 inspection cycles. Predictive maintenance intervention recommended.")
                else:
                    st.success("✓ Stable Condition: No continuous upward drift detected in recent inspection cycles.")

                # Multi-parameter Degradation Channels
                st.markdown("#### Parameter Evolution Over Time")
                c1, c2 = st.columns(2)
                with c1:
                    st.caption("Total Current Draw (A) over Dates")
                    st.line_chart(plot_df["current_A"], color=["#38bdf8"])
                    st.caption("Power Factor over Dates")
                    st.line_chart(plot_df["power_factor"], color=["#a855f7"])
                with c2:
                    st.caption("Voltage THD (%) over Dates")
                    st.line_chart(plot_df["voltage_thd"], color=["#ec4899"])
                    st.caption("Current 5th Harmonic (A) over Dates")
                    st.line_chart(plot_df["current_H5"], color=["#10b981"])

            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
            with st.expander("📄 View & Filter Historical Inspection Database"):
                st.dataframe(dev_hist if len(dev_hist) > 0 else history, use_container_width=True)
                csv_export = history.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Export Full Fleet History (CSV)",
                    data=csv_export,
                    file_name="fleet_inspection_history.csv",
                    mime="text/csv"
                )


# ==============================================================================
# VIEW 4: DEVICE BASELINE CATALOG
# ==============================================================================
elif menu == "📋 Device Baseline Catalog":
    st.markdown(f"""
    <div class="hero-banner">
        <div style="display: flex; align-items: center; gap: 16px;">
            {hero_logo_tag}
            <div>
                <h1 class="hero-title">EQUIPMENT BASELINE CATALOG</h1>
                <p class="hero-sub">Nominal baseline electrical statistics (Mean & Standard Deviation) across 25 device classes.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if baseline_stats is None:
        st.error("Baseline statistics file not found at `data/baseline_stats.csv`.")
    else:
        st.write(f"The system maintains calibrated baseline profiles for **{len(baseline_stats.index)} equipment and combination classes**.")
        
        target_device = st.selectbox("Select Baseline Profile:", sorted(baseline_stats.index))
        
        base_placeholder = st.empty()
        base_placeholder.markdown(
            f"""
            {render_skeleton_kpis()}
            {render_skeleton_table()}
            """,
            unsafe_allow_html=True
        )
        time.sleep(0.25)

        with base_placeholder.container():
            dev_profile = baseline_stats.loc[target_device]

            b1, b2, b3, b4 = st.columns(4)
            with b1:
                i1 = dev_profile.get(("I1_rms_AVG", "mean"), 0.0)
                st.metric("Nominal Line 1 Current", f"{i1:.3f} A")
            with b2:
                p = dev_profile.get(("P_sum_AVG", "mean"), 0.0)
                st.metric("Nominal Power (P_sum)", f"{p:.1f} W")
            with b3:
                pf = dev_profile.get(("PF_sum_AVG", "mean"), 0.0)
                st.metric("Nominal Power Factor", f"{abs(pf):.3f}")
            with b4:
                thd = dev_profile.get(("U1_thd-f_AVG", "mean"), 0.0)
                st.metric("Nominal Voltage THD", f"{thd:.2f}%")

            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
            st.markdown("#### Comprehensive Channel Baseline Parameters")
            records = []
            for f in feature_cols:
                m = dev_profile.get((f, "mean"), np.nan)
                s = dev_profile.get((f, "std"), np.nan)
                cat = categorize_feature(f)
                records.append({
                    "Parameter": f,
                    "Category": cat,
                    "Baseline Mean": round(m, 4) if pd.notna(m) else "N/A",
                    "Baseline Std Dev": round(s, 4) if pd.notna(s) else "N/A",
                    "Yellow Threshold": f"±{LIMITS[cat][0]*100:.1f}%",
                    "Red Threshold": f"±{LIMITS[cat][1]*100:.1f}%",
                })
            st.dataframe(pd.DataFrame(records), use_container_width=True)

            st.markdown("#### Baseline Tolerance Framework")
            st.table(pd.DataFrame([
                {"Category": k, "Yellow Limit (Warning)": f"{v[0]*100}%", "Red Limit (Critical)": f"{v[1]*100}%", "Noise Floor Cutoff": f"{MIN_CHANGE[k]}"}
                for k, v in LIMITS.items()
            ]))


# ==============================================================================
# VIEW 5: SYSTEM ARCHITECTURE & METHODOLOGY
# ==============================================================================
elif menu == "🧠 System Architecture & Methodology":
    st.markdown(f"""
    <div class="hero-banner">
        <div style="display: flex; align-items: center; gap: 16px;">
            {hero_logo_tag}
            <div>
                <h1 class="hero-title">SYSTEM ARCHITECTURE & METHODOLOGY</h1>
                <p class="hero-sub">Complete engineering workflow: high-frequency sensing, AI classification, statistical thresholding, and fleet analytics.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    arch_placeholder = st.empty()
    arch_placeholder.markdown(
        f"""
        {render_skeleton_banner()}
        {render_skeleton_table()}
        """,
        unsafe_allow_html=True
    )
    time.sleep(0.2)

    with arch_placeholder.container():
        st.markdown("""
        ### 5-Stage System Pipeline

        ```
        +---------------------------+
        | 1. High-Precision Logging |  --> 3-phase power analyzer recordings (U, I, P, PF, THD, Harmonics)
        +---------------------------+
                      │
                      ▼
        +---------------------------+
        |  2. Signal Preprocessing  |  --> Discard first 8 startup transient cycles; validate channel integrity
        +---------------------------+
                      │
                      ▼
        +---------------------------+
        | 3. Device Identification  |  --> Random Forest Classifier using 5 intrinsic load features (I1, I2, I3, P, PF)
        +---------------------------+
                      │
                      ▼
        +---------------------------+
        |  4. Early Fault Detection |  --> Dynamic Z-score & relative percentage deviation against calibrated baseline
        |                           |      Sustained run filter (>= 3 consecutive intervals / 15 seconds)
        |                           |      Grid-event vs Equipment-fault decoupling
        +---------------------------+
                      │
                      ▼
        +---------------------------+
        | 5. Actionable Diagnostics |  --> Root cause mapping (overload, winding fault, capacitor loss)
        |    & Fleet Health Trends  |      Longitudinal aging drift tracking and predictive maintenance alerts
        +---------------------------+
        ```
        """)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.subheader("Key Engineering Design Decisions")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            **1. Why 5 Features for Identification?**
            - Features: `I1_rms_AVG`, `I2_rms_AVG`, `I3_rms_AVG`, `P_sum_AVG`, `PF_sum_AVG`.
            - External grid voltage and ambient harmonics vary between labs, power outlets, and external utility loads.
            - Using intrinsic current, active power, and power factor produces a robust electrical load signature that generalizes cleanly across unseen sessions.
            """)
            st.markdown("""
            **2. Transient Filtering & False Alarm Suppression**
            - **Startup suppression**: Machine in-rush currents during the first 8 sampling intervals are safely ignored.
            - **Temporal persistence**: Anomalies must persist for at least 3 consecutive sampling cycles (15s) to avoid nuisance alerts from brief switching noise.
            """)

        with col_b:
            st.markdown("""
            **3. Decoupling Grid vs Machine Faults**
            - Changes restricted solely to Voltage, Frequency, or Voltage THD without corresponding machine current changes are classified as **External Grid Events**.
            - Internal machine faults require concurrent deviations in Current, Power, or Power Factor.
            """)
            st.markdown("""
            **4. Longitudinal Degradation Tracking**
            - Saves each completed inspection with date stamps into `data/history.csv`.
            - Tracks mean Z-score deviation over time; warns when 3 consecutive cycles show escalating health scores.
            """)

        if os.path.exists("accuracy_chart.png"):
            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
            st.subheader("Model Performance & Accuracy Benchmarks")
            st.image("accuracy_chart.png", caption="Model Validation Accuracy Benchmark Across Unseen Test Sessions")
