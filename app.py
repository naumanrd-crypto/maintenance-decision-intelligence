"""
Production Downtime & Maintenance Decision Intelligence
Industrial AI Decision-Support System
Single-file Streamlit Application: app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json
import os
import base64

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & INLINE HIGH-TECH INDUSTRIAL DARK CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Maintenance Decision Intelligence",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

MACHINE_IMAGES = {
    "M-101": "assets/hydraulic_press.jpg",
    "M-201": "assets/cnc_mill.jpg",
    "M-202": "assets/cnc_mill.jpg",
    "M-301": "assets/packaging_cell.jpg",
    "M-302": "assets/packaging_cell.jpg",
    "M-303": "assets/packaging_cell.jpg",
    "M-304": "assets/packaging_cell.jpg",
}

@st.cache_data
def get_image_base64(filepath):
    """Safely load and base64-encode image for inline zero-failure rendering."""
    if filepath and os.path.exists(filepath):
        try:
            with open(filepath, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        except Exception:
            return None
    return None

# Custom CSS for Modern Executive Light Industrial Theme
st.markdown(
    """
<style>
    /* High-Tech Industrial Clean Light Color Scheme */
    :root {
        --bg-main: #F8FAFC;
        --bg-card: #FFFFFF;
        --bg-card-alt: #F1F5F9;
        --border-subtle: #E2E8F0;
        --border-strong: #CBD5E1;
        --text-primary: #0F172A;
        --text-secondary: #334155;
        --text-muted: #64748B;
        --accent-blue: #0284C7;
        --accent-blue-light: #E0F2FE;
        --accent-cyan: #06B6D4;
        --emerald: #059669;
        --emerald-bright: #10B981;
        --emerald-bg: #ECFDF5;
        --emerald-border: #A7F3D0;
        --crimson: #DC2626;
        --crimson-bright: #EF4444;
        --crimson-bg: #FEF2F2;
        --crimson-border: #FECDD3;
        --amber: #D97706;
        --amber-bright: #F59E0B;
        --amber-bg: #FFFBEB;
        --amber-border: #FDE68A;
        --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", "Helvetica Neue", Arial, sans-serif;
    }

    /* Overall page styling */
    .stApp {
        background-color: var(--bg-main);
        color: var(--text-primary);
        font-family: var(--font-sans);
    }

    /* Sleek Executive Header Ribbon */
    .main-header-grid {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #0284C7;
        border-radius: 10px;
        padding: 16px 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }
    .header-title-box {
        flex: 1 1 480px;
    }
    .header-title-box h1 {
        font-size: 1.75rem;
        font-weight: 800;
        color: #0F172A;
        margin: 0;
        letter-spacing: -0.4px;
    }
    .header-subtitle {
        font-size: 0.9rem;
        color: #475569;
        margin-top: 3px;
        margin-bottom: 8px;
    }
    .thesis-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #E0F2FE;
        border: 1px solid #BAE6FD;
        color: #0369A1;
        font-size: 0.82rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 20px;
        font-family: var(--font-sans);
        letter-spacing: 0.15px;
    }

    /* Right-side Compact Live Plant HUD Ribbon */
    .header-hud-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 10px 18px;
        display: flex;
        gap: 20px;
        align-items: center;
        flex-wrap: wrap;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .hud-stat-item {
        display: flex;
        flex-direction: column;
    }
    .hud-label {
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: #64748B;
        font-weight: 600;
    }
    .hud-value {
        font-size: 1.08rem;
        font-weight: 700;
        font-family: var(--font-sans);
        font-feature-settings: "tnum";
        color: #0F172A;
        margin-top: 2px;
    }

    /* Top KPI Cards */
    .kpi-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-container:hover {
        border-color: #0284C7;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.1);
        transform: translateY(-2px);
    }
    .kpi-label {
        font-size: 0.78rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 800;
        font-family: var(--font-sans);
        font-feature-settings: "tnum";
        line-height: 1.2;
    }
    .kpi-subtext {
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 4px;
    }

    /* Section Cards */
    .section-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 22px;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    .section-title {
        font-size: 1.22rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 10px;
    }

    /* Machine Card Visuals */
    .topo-stage-header {
        font-size: 0.84rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #0284C7;
        margin-bottom: 10px;
        text-align: center;
    }
    .topo-node {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 12px 14px;
        text-align: left;
        transition: all 0.25s ease;
        position: relative;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .topo-node-active {
        border: 2px solid #0284C7 !important;
        box-shadow: 0 0 14px rgba(2, 132, 199, 0.25);
        background: #F0F9FF !important;
    }
    .topo-node-halted {
        border: 2px solid #EF4444 !important;
        box-shadow: 0 0 14px rgba(239, 68, 68, 0.25);
        background: #FEF2F2 !important;
    }
    .topo-node-title {
        font-size: 1rem;
        font-weight: 700;
        color: #0F172A;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .topo-node-desc {
        font-size: 0.8rem;
        color: #475569;
        margin-top: 4px;
    }
    .topo-node-meta {
        font-size: 0.76rem;
        color: #64748B;
        margin-top: 6px;
        font-family: var(--font-sans);
    }

    /* Machine Picture Styling */
    .machine-img-box {
        width: 100%;
        overflow: hidden;
        border-radius: 6px;
        margin: 8px 0;
        border: 1px solid #E2E8F0;
        background: #F8FAFC;
    }
    .machine-img {
        width: 100%;
        object-fit: cover;
        display: block;
        transition: transform 0.3s ease;
    }
    .machine-img:hover {
        transform: scale(1.03);
    }

    /* Status Pills */
    .status-pill {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.3px;
        font-family: var(--font-sans);
        font-feature-settings: "tnum";
    }
    .status-pill-green {
        background: #ECFDF5;
        color: #059669;
        border: 1px solid #A7F3D0;
    }
    .status-pill-amber {
        background: #FFFBEB;
        color: #D97706;
        border: 1px solid #FDE68A;
    }
    .status-pill-red {
        background: #FEF2F2;
        color: #DC2626;
        border: 1px solid #FECDD3;
    }

    /* Pipeline Conveyor Product Movement Animations */
    @keyframes conveyor-dash {
        0% { stroke-dashoffset: 48; }
        100% { stroke-dashoffset: 0; }
    }
    .conveyor-track {
        stroke: #CBD5E1;
        stroke-width: 5;
        fill: none;
        stroke-linecap: round;
        stroke-linejoin: round;
    }
    .flow-line-moving {
        stroke: #059669;
        stroke-width: 3.5;
        stroke-dasharray: 12, 8;
        fill: none;
        animation: conveyor-dash 1.1s linear infinite;
        filter: drop-shadow(0 0 3px rgba(5, 150, 105, 0.4));
    }
    .flow-line-stopped {
        stroke: #DC2626;
        stroke-width: 3.5;
        stroke-dasharray: 6, 6;
        fill: none;
        animation: none !important;
        filter: drop-shadow(0 0 3px rgba(220, 38, 38, 0.4));
    }
    .flow-line-starved {
        stroke: #D97706;
        stroke-width: 2.5;
        stroke-dasharray: 4, 6;
        fill: none;
        animation: none !important;
        opacity: 0.6;
    }

    /* Decision Gatekeeper Side-by-Side Cards */
    .option-card {
        border-radius: 8px;
        padding: 20px;
        height: 100%;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
    }
    .option-a-card {
        background: #F0FDF4;
        border: 1.5px solid #10B981;
    }
    .option-b-card {
        background: #FEF2F2;
        border: 1.5px solid #EF4444;
    }
    .option-b-locked {
        background: #F8FAFC !important;
        border: 1.5px dashed #94A3B8 !important;
        opacity: 0.6;
        filter: grayscale(80%);
    }
    .option-header {
        font-size: 1.22rem;
        font-weight: 700;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
        padding-bottom: 8px;
    }
    .option-a-card .option-header {
        border-bottom: 1px solid rgba(16, 185, 129, 0.2);
        color: #065F46;
    }
    .option-b-card .option-header {
        border-bottom: 1px solid rgba(239, 68, 68, 0.2);
        color: #991B1B;
    }
    .cost-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 7px 0;
        font-size: 0.9rem;
    }
    .option-a-card .cost-row {
        border-bottom: 1px solid rgba(16, 185, 129, 0.12);
        color: #166534;
    }
    .option-b-card .cost-row {
        border-bottom: 1px solid rgba(239, 68, 68, 0.12);
        color: #991B1B;
    }
    .cost-label {
        font-weight: 500;
    }
    .cost-value {
        font-family: var(--font-sans);
        font-feature-settings: "tnum";
        font-weight: 700;
        color: #0F172A;
    }
    .total-cost-box {
        margin-top: 16px;
        padding: 12px;
        border-radius: 6px;
        text-align: right;
    }
    .total-cost-box-a {
        background: #DCFCE7;
        border: 1px solid #86EFAC;
    }
    .total-cost-box-b {
        background: #FEE2E2;
        border: 1px solid #FCA5A5;
    }
    .total-cost-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 600;
    }
    .total-cost-value {
        font-size: 2rem;
        font-weight: 800;
        font-family: var(--font-sans);
        font-feature-settings: "tnum";
        line-height: 1.2;
    }

    /* Net Decision Banner */
    .net-decision-banner {
        background: linear-gradient(90deg, #ECFDF5 0%, #F0FDF4 100%);
        border: 1.5px solid #10B981;
        border-radius: 8px;
        padding: 18px 24px;
        margin: 18px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 10px rgba(16, 185, 129, 0.1);
    }
    .net-banner-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #065F46;
    }
    .net-banner-sub {
        font-size: 0.88rem;
        color: #047857;
        margin-top: 4px;
    }
    .net-banner-metrics {
        display: flex;
        gap: 28px;
        text-align: right;
    }
    .net-metric-num {
        font-size: 1.95rem;
        font-weight: 800;
        font-family: var(--font-sans);
        font-feature-settings: "tnum";
        color: #059669;
    }
    .net-metric-lbl {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #065F46;
    }

    /* Statutory Safety Alert Banner */
    .safety-alert-banner {
        background: #FEF2F2;
        border: 2px solid #DC2626;
        border-radius: 8px;
        padding: 18px 24px;
        margin: 18px 0;
        box-shadow: 0 2px 12px rgba(220, 38, 38, 0.1);
    }
    .safety-alert-title {
        font-size: 1.22rem;
        font-weight: 800;
        color: #991B1B;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .safety-alert-body {
        font-size: 0.92rem;
        color: #7F1D1D;
        margin-top: 8px;
        line-height: 1.5;
    }

    /* Diagnostic Callout Header */
    .diagnostic-header {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #0284C7;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 18px;
        display: grid;
        grid-template-columns: 1fr auto;
        gap: 20px;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .diag-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0F172A;
    }
    .diag-meta {
        font-size: 0.85rem;
        color: #475569;
        margin-top: 6px;
    }

    /* Mode Selection Cards */
    .mode-select-card {
        background: #FFFFFF;
        border: 2px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px 20px;
        transition: all 0.25s ease;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    .mode-select-card:hover {
        border-color: #0284C7;
        box-shadow: 0 8px 24px rgba(2, 132, 199, 0.12);
        transform: translateY(-3px);
    }
    .mode-card-icon {
        font-size: 2.4rem;
        margin-bottom: 12px;
    }
    .mode-card-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 6px;
    }
    .mode-card-desc {
        font-size: 0.88rem;
        color: #64748B;
        line-height: 1.5;
        margin-bottom: 16px;
        flex-grow: 1;
    }

    /* Header Styling */
    .simple-header {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #0284C7;
        border-radius: 10px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .simple-header h1 {
        font-size: 1.75rem;
        font-weight: 800;
        color: #0F172A;
        margin: 0;
        letter-spacing: -0.4px;
    }
    .header-subtitle {
        font-size: 0.92rem;
        color: #475569;
        margin-top: 4px;
        margin-bottom: 10px;
    }

    /* Complete High-Contrast Light Theme Button Overrides */
    button,
    div.stButton > button,
    div.stDownloadButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        font-family: var(--font-sans) !important;
        transition: all 0.2s ease !important;
    }

    /* All Standard & Secondary Buttons (Clean White Card Style with High Contrast Text) */
    button:not([kind="primary"]),
    div.stButton > button:not([kind="primary"]),
    div.stDownloadButton > button:not([kind="primary"]),
    button[kind="secondary"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #0F172A !important;
        border: 1.5px solid #CBD5E1 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }
    button:not([kind="primary"]):hover,
    div.stButton > button:not([kind="primary"]):hover,
    div.stDownloadButton > button:not([kind="primary"]):hover,
    button[kind="secondary"]:hover {
        background-color: #F8FAFC !important;
        background: #F8FAFC !important;
        color: #0284C7 !important;
        border-color: #0284C7 !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.15) !important;
    }
    button:not([kind="primary"]):active,
    div.stButton > button:not([kind="primary"]):active,
    button[kind="secondary"]:active {
        background-color: #E2E8F0 !important;
        background: #E2E8F0 !important;
    }

    /* Primary Action Buttons (Vibrant Ocean Blue with Pure White Text) */
    button[kind="primary"],
    div.stButton > button[kind="primary"],
    div.stDownloadButton > button[kind="primary"] {
        background-color: #0284C7 !important;
        background: #0284C7 !important;
        color: #FFFFFF !important;
        border: 1.5px solid #0284C7 !important;
        box-shadow: 0 2px 8px rgba(2, 132, 199, 0.25) !important;
    }
    button[kind="primary"]:hover,
    div.stButton > button[kind="primary"]:hover,
    div.stDownloadButton > button[kind="primary"]:hover {
        background-color: #0369A1 !important;
        background: #0369A1 !important;
        border-color: #0369A1 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35) !important;
    }

    /* Ensure text inside button paragraphs/spans inherits high-contrast color */
    button p,
    button span,
    div.stButton > button p,
    div.stButton > button span {
        color: inherit !important;
        font-weight: 600 !important;
    }

    /* Selectboxes and Inputs */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {
        color: #0F172A !important;
    }

    /* Text Inputs */
    div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="input"] input {
        color: #0F172A !important;
        background-color: #FFFFFF !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. MASTER EMBEDDED DATASET & ROBUST INGESTION LAYER
# -----------------------------------------------------------------------------
FALLBACK_ASSETS = [
    {
        "Machine_ID": "M-101",
        "Stage": 1,
        "Process": "Primary Forming",
        "Machine_Type": "Hydraulic Stamping Press",
        "Capacity_pkts_hr": 100,
        "Line_Loss_Rate_PKR_hr": 180000,
        "Operator_Assignment": "Tariq M. (Lead Operator); Kashif R. (Press Feeder)",
        "Failure_Topology": "Single point of failure",
        "Throughput_Loss_if_Trip_pct": 100,
        "Failure_Rule": "Single point of failure. If M-101 trips, 100% of plant output is lost immediately.",
    },
    {
        "Machine_ID": "M-201",
        "Stage": 2,
        "Process": "Milling",
        "Machine_Type": "High-Speed CNC Milling Center",
        "Capacity_pkts_hr": 50,
        "Line_Loss_Rate_PKR_hr": 120000,
        "Operator_Assignment": "Salman A. (Machinist)",
        "Failure_Topology": "Parallel split",
        "Throughput_Loss_if_Trip_pct": 50,
        "Failure_Rule": "Parallel split. If M-201 trips, M-202 remains online; overall plant throughput drops by 50%, while M-301 and M-302 starve for work.",
    },
    {
        "Machine_ID": "M-202",
        "Stage": 2,
        "Process": "Milling",
        "Machine_Type": "High-Speed CNC Milling Center",
        "Capacity_pkts_hr": 50,
        "Line_Loss_Rate_PKR_hr": 120000,
        "Operator_Assignment": "Imran P. (Machinist)",
        "Failure_Topology": "Parallel split",
        "Throughput_Loss_if_Trip_pct": 50,
        "Failure_Rule": "Parallel split. If M-202 trips, M-201 remains online; overall plant throughput drops by 50%, while M-303 and M-304 starve for work.",
    },
    {
        "Machine_ID": "M-301",
        "Stage": 3,
        "Process": "Packaging",
        "Machine_Type": "Automated Packaging Cell",
        "Capacity_pkts_hr": 25,
        "Line_Loss_Rate_PKR_hr": 45000,
        "Operator_Assignment": "Zahid H. (Operator, Line A)",
        "Failure_Topology": "Quad split",
        "Throughput_Loss_if_Trip_pct": 25,
        "Failure_Rule": "Quad split. If this packaging cell trips, plant throughput drops by 25%; the other three cells remain online.",
    },
    {
        "Machine_ID": "M-302",
        "Stage": 3,
        "Process": "Packaging",
        "Machine_Type": "Automated Packaging Cell",
        "Capacity_pkts_hr": 25,
        "Line_Loss_Rate_PKR_hr": 45000,
        "Operator_Assignment": "Zahid H. (Operator, Line A)",
        "Failure_Topology": "Quad split",
        "Throughput_Loss_if_Trip_pct": 25,
        "Failure_Rule": "Quad split. If this packaging cell trips, plant throughput drops by 25%; the other three cells remain online.",
    },
    {
        "Machine_ID": "M-303",
        "Stage": 3,
        "Process": "Packaging",
        "Machine_Type": "Automated Packaging Cell",
        "Capacity_pkts_hr": 25,
        "Line_Loss_Rate_PKR_hr": 45000,
        "Operator_Assignment": "Bilal N. (Operator, Line B)",
        "Failure_Topology": "Quad split",
        "Throughput_Loss_if_Trip_pct": 25,
        "Failure_Rule": "Quad split. If this packaging cell trips, plant throughput drops by 25%; the other three cells remain online.",
    },
    {
        "Machine_ID": "M-304",
        "Stage": 3,
        "Process": "Packaging",
        "Machine_Type": "Automated Packaging Cell",
        "Capacity_pkts_hr": 25,
        "Line_Loss_Rate_PKR_hr": 45000,
        "Operator_Assignment": "Bilal N. (Operator, Line B)",
        "Failure_Topology": "Quad split",
        "Throughput_Loss_if_Trip_pct": 25,
        "Failure_Rule": "Quad split. If this packaging cell trips, plant throughput drops by 25%; the other three cells remain online.",
    },
]

FALLBACK_ERROR_MATRIX = [
    {
        "Error_ID": "M1-E01",
        "Stage": 1,
        "Applicable_Machines": "M-101",
        "Machine_Type": "Hydraulic Stamping Press",
        "Failure_Category": "Mechanical",
        "Failure_Mode": "Hydraulic Seal Weeping",
        "Symptom": "Oil weeping along main cylinder rod.",
        "Safety_Critical": False,
        "Safety_Message": None,
        "Line_Loss_Rate_PKR_hr": 180000,
        "Planned_Downtime_min": 15,
        "Planned_Production_Loss_PKR": 45000,
        "OptionA_Part_Description": "O-Ring Kit",
        "OptionA_Part_Cost_PKR": 8500,
        "OptionA_Labor_Cost_PKR": 3000,
        "OptionA_Total_PKR": 56500,
        "Unplanned_Downtime_min": 180,
        "Unplanned_Production_Loss_PKR": 540000,
        "OptionB_Replacement_Description": "Ram Replacement",
        "OptionB_Replacement_Cost_PKR": 145000,
        "OptionB_Freight_PKR": 45000,
        "OptionB_Idle_Operator_Cost_PKR": 18000,
        "OptionB_Emergency_Tech_Cost_PKR": 25000,
        "OptionB_Scrap_Description": "Scrap Waste",
        "OptionB_Scrap_Cost_PKR": 35000,
        "OptionB_Total_PKR": 808000,
        "Net_Avoided_Loss_PKR": 751500,
        "Decision_Status": "INTERVENE NOW",
    },
    {
        "Error_ID": "M1-E02",
        "Stage": 1,
        "Applicable_Machines": "M-101",
        "Machine_Type": "Hydraulic Stamping Press",
        "Failure_Category": "Electrical",
        "Failure_Mode": "Motor Terminal Overheating",
        "Symptom": "High-resistance lug hot spot (88°C).",
        "Safety_Critical": False,
        "Safety_Message": None,
        "Line_Loss_Rate_PKR_hr": 180000,
        "Planned_Downtime_min": 10,
        "Planned_Production_Loss_PKR": 30000,
        "OptionA_Part_Description": "Cable Lugs",
        "OptionA_Part_Cost_PKR": 4000,
        "OptionA_Labor_Cost_PKR": 2500,
        "OptionA_Total_PKR": 36500,
        "Unplanned_Downtime_min": 120,
        "Unplanned_Production_Loss_PKR": 360000,
        "OptionB_Replacement_Description": "75 kW Motor Rewind",
        "OptionB_Replacement_Cost_PKR": 180000,
        "OptionB_Freight_PKR": 25000,
        "OptionB_Idle_Operator_Cost_PKR": 12000,
        "OptionB_Emergency_Tech_Cost_PKR": 30000,
        "OptionB_Scrap_Description": "Scrap Waste",
        "OptionB_Scrap_Cost_PKR": 15000,
        "OptionB_Total_PKR": 622000,
        "Net_Avoided_Loss_PKR": 585500,
        "Decision_Status": "INTERVENE NOW",
    },
    {
        "Error_ID": "M1-E03",
        "Stage": 1,
        "Applicable_Machines": "M-101",
        "Machine_Type": "Hydraulic Stamping Press",
        "Failure_Category": "Mechanical",
        "Failure_Mode": "Flywheel Bushing Wear",
        "Symptom": "Vibration harmonic during stroke.",
        "Safety_Critical": False,
        "Safety_Message": None,
        "Line_Loss_Rate_PKR_hr": 180000,
        "Planned_Downtime_min": 20,
        "Planned_Production_Loss_PKR": 60000,
        "OptionA_Part_Description": "Bronze Bush",
        "OptionA_Part_Cost_PKR": 12000,
        "OptionA_Labor_Cost_PKR": 4000,
        "OptionA_Total_PKR": 76000,
        "Unplanned_Downtime_min": 240,
        "Unplanned_Production_Loss_PKR": 720000,
        "OptionB_Replacement_Description": "Drive Shaft Core",
        "OptionB_Replacement_Cost_PKR": 320000,
        "OptionB_Freight_PKR": 75000,
        "OptionB_Idle_Operator_Cost_PKR": 24000,
        "OptionB_Emergency_Tech_Cost_PKR": 40000,
        "OptionB_Scrap_Description": "Scrap Waste",
        "OptionB_Scrap_Cost_PKR": 50000,
        "OptionB_Total_PKR": 1229000,
        "Net_Avoided_Loss_PKR": 1153000,
        "Decision_Status": "INTERVENE NOW",
    },
    {
        "Error_ID": "M1-E04",
        "Stage": 1,
        "Applicable_Machines": "M-101",
        "Machine_Type": "Hydraulic Stamping Press",
        "Failure_Category": "Safety",
        "Failure_Mode": "Light Curtain Alignment",
        "Symptom": "Optical sensor misalignment trip.",
        "Safety_Critical": True,
        "Safety_Message": "MANDATORY SAFETY OVERRIDE: Option B locked out. Operating with an unaligned safety curtain violates statutory safety codes. Immediate shutdown enforced.",
        "Line_Loss_Rate_PKR_hr": 180000,
        "Planned_Downtime_min": 10,
        "Planned_Production_Loss_PKR": 30000,
        "OptionA_Part_Description": "Bracket Kit",
        "OptionA_Part_Cost_PKR": 5000,
        "OptionA_Labor_Cost_PKR": 2000,
        "OptionA_Total_PKR": 37000,
        "Unplanned_Downtime_min": None,
        "Unplanned_Production_Loss_PKR": None,
        "OptionB_Replacement_Description": "LOCKED OUT",
        "OptionB_Replacement_Cost_PKR": None,
        "OptionB_Freight_PKR": None,
        "OptionB_Idle_Operator_Cost_PKR": None,
        "OptionB_Emergency_Tech_Cost_PKR": None,
        "OptionB_Scrap_Description": "Not Applicable",
        "OptionB_Scrap_Cost_PKR": None,
        "OptionB_Total_PKR": None,
        "Net_Avoided_Loss_PKR": None,
        "Decision_Status": "MANDATORY SAFETY OVERRIDE",
    },
    {
        "Error_ID": "M1-E05",
        "Stage": 1,
        "Applicable_Machines": "M-101",
        "Machine_Type": "Hydraulic Stamping Press",
        "Failure_Category": "Mechanical",
        "Failure_Mode": "Punch Die Micro-Cracking",
        "Symptom": "Workpiece burr height exceeds 0.2 mm.",
        "Safety_Critical": False,
        "Safety_Message": None,
        "Line_Loss_Rate_PKR_hr": 180000,
        "Planned_Downtime_min": 25,
        "Planned_Production_Loss_PKR": 75000,
        "OptionA_Part_Description": "Insert Set",
        "OptionA_Part_Cost_PKR": 18000,
        "OptionA_Labor_Cost_PKR": 5000,
        "OptionA_Total_PKR": 98000,
        "Unplanned_Downtime_min": 210,
        "Unplanned_Production_Loss_PKR": 630000,
        "OptionB_Replacement_Description": "Complete Die Tool",
        "OptionB_Replacement_Cost_PKR": 480000,
        "OptionB_Freight_PKR": 60000,
        "OptionB_Idle_Operator_Cost_PKR": 21000,
        "OptionB_Emergency_Tech_Cost_PKR": 45000,
        "OptionB_Scrap_Description": "Tooling Scrap",
        "OptionB_Scrap_Cost_PKR": 120000,
        "OptionB_Total_PKR": 1356000,
        "Net_Avoided_Loss_PKR": 1258000,
        "Decision_Status": "INTERVENE NOW",
    },
    {
        "Error_ID": "M2-E01",
        "Stage": 2,
        "Applicable_Machines": "M-201; M-202",
        "Machine_Type": "High-Speed CNC Milling Center",
        "Failure_Category": "Mechanical",
        "Failure_Mode": "Ceramic Bearing Wear",
        "Symptom": "Spindle runout 12 µm with acoustic whine.",
        "Safety_Critical": False,
        "Safety_Message": None,
        "Line_Loss_Rate_PKR_hr": 120000,
        "Planned_Downtime_min": 20,
        "Planned_Production_Loss_PKR": 40000,
        "OptionA_Part_Description": "Bearing Kit",
        "OptionA_Part_Cost_PKR": 35000,
        "OptionA_Labor_Cost_PKR": 4000,
        "OptionA_Total_PKR": 79000,
        "Unplanned_Downtime_min": 300,
        "Unplanned_Production_Loss_PKR": 600000,
        "OptionB_Replacement_Description": "Spindle Core",
        "OptionB_Replacement_Cost_PKR": 650000,
        "OptionB_Freight_PKR": 110000,
        "OptionB_Idle_Operator_Cost_PKR": 24000,
        "OptionB_Emergency_Tech_Cost_PKR": 50000,
        "OptionB_Scrap_Description": "Scrap Part",
        "OptionB_Scrap_Cost_PKR": 85000,
        "OptionB_Total_PKR": 1519000,
        "Net_Avoided_Loss_PKR": 1440000,
        "Decision_Status": "INTERVENE NOW",
    },
    {
        "Error_ID": "M2-E02",
        "Stage": 2,
        "Applicable_Machines": "M-201; M-202",
        "Machine_Type": "High-Speed CNC Milling Center",
        "Failure_Category": "Electrical",
        "Failure_Mode": "Servo Encoder Jitter",
        "Symptom": "Sinamics drive tracking warning.",
        "Safety_Critical": False,
        "Safety_Message": None,
        "Line_Loss_Rate_PKR_hr": 120000,
        "Planned_Downtime_min": 15,
        "Planned_Production_Loss_PKR": 30000,
        "OptionA_Part_Description": "Feedback Lead",
        "OptionA_Part_Cost_PKR": 14000,
        "OptionA_Labor_Cost_PKR": 3500,
        "OptionA_Total_PKR": 47500,
        "Unplanned_Downtime_min": 150,
        "Unplanned_Production_Loss_PKR": 300000,
        "OptionB_Replacement_Description": "Servo Motor Package",
        "OptionB_Replacement_Cost_PKR": 290000,
        "OptionB_Freight_PKR": 50000,
        "OptionB_Idle_Operator_Cost_PKR": 12000,
        "OptionB_Emergency_Tech_Cost_PKR": 30000,
        "OptionB_Scrap_Description": "Scrap Part",
        "OptionB_Scrap_Cost_PKR": 95000,
        "OptionB_Total_PKR": 777000,
        "Net_Avoided_Loss_PKR": 729500,
        "Decision_Status": "INTERVENE NOW",
    },
    {
        "Error_ID": "M2-E03",
        "Stage": 2,
        "Applicable_Machines": "M-201; M-202",
        "Machine_Type": "High-Speed CNC Milling Center",
        "Failure_Category": "Mechanical",
        "Failure_Mode": "Pump Cavitation",
        "Symptom": "Coolant line pressure dips below 3 bar.",
        "Safety_Critical": False,
        "Safety_Message": None,
        "Line_Loss_Rate_PKR_hr": 120000,
        "Planned_Downtime_min": 10,
        "Planned_Production_Loss_PKR": 20000,
        "OptionA_Part_Description": "Gasket & Strainer",
        "OptionA_Part_Cost_PKR": 6000,
        "OptionA_Labor_Cost_PKR": 2000,
        "OptionA_Total_PKR": 28000,
        "Unplanned_Downtime_min": 110,
        "Unplanned_Production_Loss_PKR": 220000,
        "OptionB_Replacement_Description": "Multi-stage Pump",
        "OptionB_Replacement_Cost_PKR": 130000,
        "OptionB_Freight_PKR": 25000,
        "OptionB_Idle_Operator_Cost_PKR": 8800,
        "OptionB_Emergency_Tech_Cost_PKR": 18000,
        "OptionB_Scrap_Description": "Burned Scrap",
        "OptionB_Scrap_Cost_PKR": 40000,
        "OptionB_Total_PKR": 441800,
        "Net_Avoided_Loss_PKR": 413800,
        "Decision_Status": "INTERVENE NOW",
    },
    {
        "Error_ID": "M2-E04",
        "Stage": 2,
        "Applicable_Machines": "M-201; M-202",
        "Machine_Type": "High-Speed CNC Milling Center",
        "Failure_Category": "Electrical",
        "Failure_Mode": "Solenoid Overheating",
        "Symptom": "Tool changer arm cycle delay > 1.8 s.",
        "Safety_Critical": False,
        "Safety_Message": None,
        "Line_Loss_Rate_PKR_hr": 120000,
        "Planned_Downtime_min": 10,
        "Planned_Production_Loss_PKR": 20000,
        "OptionA_Part_Description": "24 V Solenoid",
        "OptionA_Part_Cost_PKR": 7500,
        "OptionA_Labor_Cost_PKR": 2500,
        "OptionA_Total_PKR": 30000,
        "Unplanned_Downtime_min": 140,
        "Unplanned_Production_Loss_PKR": 280000,
        "OptionB_Replacement_Description": "Gripper Assembly",
        "OptionB_Replacement_Cost_PKR": 340000,
        "OptionB_Freight_PKR": 60000,
        "OptionB_Idle_Operator_Cost_PKR": 11200,
        "OptionB_Emergency_Tech_Cost_PKR": 25000,
        "OptionB_Scrap_Description": "Fixture Scrap",
        "OptionB_Scrap_Cost_PKR": 65000,
        "OptionB_Total_PKR": 781200,
        "Net_Avoided_Loss_PKR": 751200,
        "Decision_Status": "INTERVENE NOW",
    },
    {
        "Error_ID": "M2-E05",
        "Stage": 2,
        "Applicable_Machines": "M-201; M-202",
        "Machine_Type": "High-Speed CNC Milling Center",
        "Failure_Category": "Safety",
        "Failure_Mode": "Enclosure Interlock Fault",
        "Symptom": "Spindle continues spinning with door open.",
        "Safety_Critical": True,
        "Safety_Message": "MANDATORY SAFETY OVERRIDE: Option B locked out. Operating with an unverified interlock switch violates machine safeguarding regulations.",
        "Line_Loss_Rate_PKR_hr": 120000,
        "Planned_Downtime_min": 10,
        "Planned_Production_Loss_PKR": 20000,
        "OptionA_Part_Description": "Magnetic Switch",
        "OptionA_Part_Cost_PKR": 9000,
        "OptionA_Labor_Cost_PKR": 2500,
        "OptionA_Total_PKR": 31500,
        "Unplanned_Downtime_min": None,
        "Unplanned_Production_Loss_PKR": None,
        "OptionB_Replacement_Description": "LOCKED OUT",
        "OptionB_Replacement_Cost_PKR": None,
        "OptionB_Freight_PKR": None,
        "OptionB_Idle_Operator_Cost_PKR": None,
        "OptionB_Emergency_Tech_Cost_PKR": None,
        "OptionB_Scrap_Description": "Not Applicable",
        "OptionB_Scrap_Cost_PKR": None,
        "OptionB_Total_PKR": None,
        "Net_Avoided_Loss_PKR": None,
        "Decision_Status": "MANDATORY SAFETY OVERRIDE",
    },
    {
        "Error_ID": "M3-E01",
        "Stage": 3,
        "Applicable_Machines": "M-301; M-302; M-303; M-304",
        "Machine_Type": "Automated Packaging Cell",
        "Failure_Category": "Mechanical",
        "Failure_Mode": "Conveyor Belt Skew",
        "Symptom": "Belt edge rubbing side chassis guide.",
        "Safety_Critical": False,
        "Safety_Message": None,
        "Line_Loss_Rate_PKR_hr": 45000,
        "Planned_Downtime_min": 15,
        "Planned_Production_Loss_PKR": 11250,
        "OptionA_Part_Description": "Guide Collar",
        "OptionA_Part_Cost_PKR": 5000,
        "OptionA_Labor_Cost_PKR": 2500,
        "OptionA_Total_PKR": 18750,
        "Unplanned_Downtime_min": 90,
        "Unplanned_Production_Loss_PKR": 67500,
        "OptionB_Replacement_Description": "Vulcanized Belt",
        "OptionB_Replacement_Cost_PKR": 78000,
        "OptionB_Freight_PKR": 20000,
        "OptionB_Idle_Operator_Cost_PKR": 6000,
        "OptionB_Emergency_Tech_Cost_PKR": 14000,
        "OptionB_Scrap_Description": "Crushed Cartons",
        "OptionB_Scrap_Cost_PKR": 22000,
        "OptionB_Total_PKR": 207500,
        "Net_Avoided_Loss_PKR": 188750,
        "Decision_Status": "INTERVENE NOW",
    },
    {
        "Error_ID": "M3-E02",
        "Stage": 3,
        "Applicable_Machines": "M-301; M-302; M-303; M-304",
        "Machine_Type": "Automated Packaging Cell",
        "Failure_Category": "Electrical",
        "Failure_Mode": "Vacuum Sensor Drift",
        "Symptom": "Negative pressure fluctuations during case pick.",
        "Safety_Critical": False,
        "Safety_Message": None,
        "Line_Loss_Rate_PKR_hr": 45000,
        "Planned_Downtime_min": 10,
        "Planned_Production_Loss_PKR": 7500,
        "OptionA_Part_Description": "Cup/Filter Kit",
        "OptionA_Part_Cost_PKR": 4500,
        "OptionA_Labor_Cost_PKR": 2000,
        "OptionA_Total_PKR": 14000,
        "Unplanned_Downtime_min": 75,
        "Unplanned_Production_Loss_PKR": 56250,
        "OptionB_Replacement_Description": "Venturi Vacuum Unit",
        "OptionB_Replacement_Cost_PKR": 85000,
        "OptionB_Freight_PKR": 18000,
        "OptionB_Idle_Operator_Cost_PKR": 5000,
        "OptionB_Emergency_Tech_Cost_PKR": 12000,
        "OptionB_Scrap_Description": "Ruined Stock",
        "OptionB_Scrap_Cost_PKR": 48000,
        "OptionB_Total_PKR": 224250,
        "Net_Avoided_Loss_PKR": 210250,
        "Decision_Status": "INTERVENE NOW",
    },
    {
        "Error_ID": "M3-E03",
        "Stage": 3,
        "Applicable_Machines": "M-301; M-302; M-303; M-304",
        "Machine_Type": "Automated Packaging Cell",
        "Failure_Category": "Mechanical",
        "Failure_Mode": "Nozzle Carbonization",
        "Symptom": "Adhesive stringing and partial glue flap bead.",
        "Safety_Critical": False,
        "Safety_Message": None,
        "Line_Loss_Rate_PKR_hr": 45000,
        "Planned_Downtime_min": 10,
        "Planned_Production_Loss_PKR": 7500,
        "OptionA_Part_Description": "Brass Nozzle",
        "OptionA_Part_Cost_PKR": 6000,
        "OptionA_Labor_Cost_PKR": 2000,
        "OptionA_Total_PKR": 15500,
        "Unplanned_Downtime_min": 80,
        "Unplanned_Production_Loss_PKR": 60000,
        "OptionB_Replacement_Description": "Heated Manifold Head",
        "OptionB_Replacement_Cost_PKR": 115000,
        "OptionB_Freight_PKR": 22000,
        "OptionB_Idle_Operator_Cost_PKR": 5300,
        "OptionB_Emergency_Tech_Cost_PKR": 14000,
        "OptionB_Scrap_Description": "Batch Scrap",
        "OptionB_Scrap_Cost_PKR": 15000,
        "OptionB_Total_PKR": 231300,
        "Net_Avoided_Loss_PKR": 215800,
        "Decision_Status": "INTERVENE NOW",
    },
    {
        "Error_ID": "M3-E04",
        "Stage": 3,
        "Applicable_Machines": "M-301; M-302; M-303; M-304",
        "Machine_Type": "Automated Packaging Cell",
        "Failure_Category": "Electrical",
        "Failure_Mode": "Scanner Link Timeout",
        "Symptom": "EtherNet/IP dropped packets freeze sorting.",
        "Safety_Critical": False,
        "Safety_Message": None,
        "Line_Loss_Rate_PKR_hr": 45000,
        "Planned_Downtime_min": 10,
        "Planned_Production_Loss_PKR": 7500,
        "OptionA_Part_Description": "Shielded Cable",
        "OptionA_Part_Cost_PKR": 7000,
        "OptionA_Labor_Cost_PKR": 2000,
        "OptionA_Total_PKR": 16500,
        "Unplanned_Downtime_min": 60,
        "Unplanned_Production_Loss_PKR": 45000,
        "OptionB_Replacement_Description": "Laser Imager Unit",
        "OptionB_Replacement_Cost_PKR": 165000,
        "OptionB_Freight_PKR": 28000,
        "OptionB_Idle_Operator_Cost_PKR": 4000,
        "OptionB_Emergency_Tech_Cost_PKR": 12000,
        "OptionB_Scrap_Description": "Re-label Scrap",
        "OptionB_Scrap_Cost_PKR": 5000,
        "OptionB_Total_PKR": 259000,
        "Net_Avoided_Loss_PKR": 242500,
        "Decision_Status": "INTERVENE NOW",
    },
    {
        "Error_ID": "M3-E05",
        "Stage": 3,
        "Applicable_Machines": "M-301; M-302; M-303; M-304",
        "Machine_Type": "Automated Packaging Cell",
        "Failure_Category": "Safety",
        "Failure_Mode": "E-Stop Ground Fault",
        "Symptom": "Emergency loop fails continuity self-test.",
        "Safety_Critical": True,
        "Safety_Message": "MANDATORY SAFETY OVERRIDE: Option B locked out. Compromised emergency circuits prevent legal operation under statutory safety law.",
        "Line_Loss_Rate_PKR_hr": 45000,
        "Planned_Downtime_min": 10,
        "Planned_Production_Loss_PKR": 7500,
        "OptionA_Part_Description": "Safety Contact",
        "OptionA_Part_Cost_PKR": 6500,
        "OptionA_Labor_Cost_PKR": 2000,
        "OptionA_Total_PKR": 16000,
        "Unplanned_Downtime_min": None,
        "Unplanned_Production_Loss_PKR": None,
        "OptionB_Replacement_Description": "LOCKED OUT",
        "OptionB_Replacement_Cost_PKR": None,
        "OptionB_Freight_PKR": None,
        "OptionB_Idle_Operator_Cost_PKR": None,
        "OptionB_Emergency_Tech_Cost_PKR": None,
        "OptionB_Scrap_Description": "Not Applicable",
        "OptionB_Scrap_Cost_PKR": None,
        "OptionB_Total_PKR": None,
        "Net_Avoided_Loss_PKR": None,
        "Decision_Status": "MANDATORY SAFETY OVERRIDE",
    },
]

FALLBACK_HISTORICAL_EVENTS = [
    {
        "Event_Date": "2026-07-05",
        "Month_Key": "2026-07",
        "Machine_ID": "M-101",
        "Error_ID": "M1-E02",
        "Stage": 1,
        "Failure_Category": "Electrical",
        "Failure_Mode": "Motor Terminal Overheating",
        "Reported_By": "Tariq M.",
        "Shift": "A",
        "Decision": "Accept Option A",
        "Safety_Override": "No",
        "Planned_Stop_Min": 10,
        "Unplanned_Downtime_Min": 120.0,
        "OptionA_Total_PKR": 36500,
        "OptionB_Total_PKR": 622000.0,
        "Net_Avoided_Loss_PKR": 585500.0,
        "Production_Hours_Rescued": 1.833333,
        "Notes": "Preventive intervention approved after Option A vs Option B cost comparison.",
    },
    {
        "Event_Date": "2026-07-12",
        "Month_Key": "2026-07",
        "Machine_ID": "M-201",
        "Error_ID": "M2-E01",
        "Stage": 2,
        "Failure_Category": "Mechanical",
        "Failure_Mode": "Ceramic Bearing Wear",
        "Reported_By": "Salman A.",
        "Shift": "B",
        "Decision": "Accept Option A",
        "Safety_Override": "No",
        "Planned_Stop_Min": 20,
        "Unplanned_Downtime_Min": 300.0,
        "OptionA_Total_PKR": 79000,
        "OptionB_Total_PKR": 1519000.0,
        "Net_Avoided_Loss_PKR": 1440000.0,
        "Production_Hours_Rescued": 4.666667,
        "Notes": "Preventive intervention approved after Option A vs Option B cost comparison.",
    },
    {
        "Event_Date": "2026-07-18",
        "Month_Key": "2026-07",
        "Machine_ID": "M-202",
        "Error_ID": "M2-E02",
        "Stage": 2,
        "Failure_Category": "Electrical",
        "Failure_Mode": "Servo Encoder Jitter",
        "Reported_By": "Imran P.",
        "Shift": "A",
        "Decision": "Accept Option A",
        "Safety_Override": "No",
        "Planned_Stop_Min": 15,
        "Unplanned_Downtime_Min": 150.0,
        "OptionA_Total_PKR": 47500,
        "OptionB_Total_PKR": 777000.0,
        "Net_Avoided_Loss_PKR": 729500.0,
        "Production_Hours_Rescued": 2.250000,
        "Notes": "Preventive intervention approved after Option A vs Option B cost comparison.",
    },
    {
        "Event_Date": "2026-07-26",
        "Month_Key": "2026-07",
        "Machine_ID": "M-302",
        "Error_ID": "M3-E01",
        "Stage": 3,
        "Failure_Category": "Mechanical",
        "Failure_Mode": "Conveyor Belt Skew",
        "Reported_By": "Zahid H.",
        "Shift": "C",
        "Decision": "Accept Option A",
        "Safety_Override": "No",
        "Planned_Stop_Min": 15,
        "Unplanned_Downtime_Min": 90.0,
        "OptionA_Total_PKR": 18750,
        "OptionB_Total_PKR": 207500.0,
        "Net_Avoided_Loss_PKR": 188750.0,
        "Production_Hours_Rescued": 1.250000,
        "Notes": "Preventive intervention approved after Option A vs Option B cost comparison.",
    },
    {
        "Event_Date": "2026-07-30",
        "Month_Key": "2026-07",
        "Machine_ID": "M-101",
        "Error_ID": "M1-E04",
        "Stage": 1,
        "Failure_Category": "Safety",
        "Failure_Mode": "Light Curtain Alignment",
        "Reported_By": "Kashif R.",
        "Shift": "B",
        "Decision": "Mandatory Stop",
        "Safety_Override": "Yes",
        "Planned_Stop_Min": 10,
        "Unplanned_Downtime_Min": 0.0,
        "OptionA_Total_PKR": 37000,
        "OptionB_Total_PKR": 0.0,
        "Net_Avoided_Loss_PKR": 0.0,
        "Production_Hours_Rescued": 0.0,
        "Notes": "Safety-critical condition. Economic deferral prohibited; immediate intervention enforced.",
    },
    {
        "Event_Date": "2026-08-03",
        "Month_Key": "2026-08",
        "Machine_ID": "M-101",
        "Error_ID": "M1-E03",
        "Stage": 1,
        "Failure_Category": "Mechanical",
        "Failure_Mode": "Flywheel Bushing Wear",
        "Reported_By": "Tariq M.",
        "Shift": "A",
        "Decision": "Accept Option A",
        "Safety_Override": "No",
        "Planned_Stop_Min": 20,
        "Unplanned_Downtime_Min": 240.0,
        "OptionA_Total_PKR": 76000,
        "OptionB_Total_PKR": 1229000.0,
        "Net_Avoided_Loss_PKR": 1153000.0,
        "Production_Hours_Rescued": 3.666667,
        "Notes": "Preventive intervention approved after Option A vs Option B cost comparison.",
    },
    {
        "Event_Date": "2026-08-09",
        "Month_Key": "2026-08",
        "Machine_ID": "M-101",
        "Error_ID": "M1-E05",
        "Stage": 1,
        "Failure_Category": "Mechanical",
        "Failure_Mode": "Punch Die Micro-Cracking",
        "Reported_By": "Kashif R.",
        "Shift": "B",
        "Decision": "Accept Option A",
        "Safety_Override": "No",
        "Planned_Stop_Min": 25,
        "Unplanned_Downtime_Min": 210.0,
        "OptionA_Total_PKR": 98000,
        "OptionB_Total_PKR": 1356000.0,
        "Net_Avoided_Loss_PKR": 1258000.0,
        "Production_Hours_Rescued": 3.083333,
        "Notes": "Preventive intervention approved after Option A vs Option B cost comparison.",
    },
    {
        "Event_Date": "2026-08-15",
        "Month_Key": "2026-08",
        "Machine_ID": "M-201",
        "Error_ID": "M2-E02",
        "Stage": 2,
        "Failure_Category": "Electrical",
        "Failure_Mode": "Servo Encoder Jitter",
        "Reported_By": "Salman A.",
        "Shift": "C",
        "Decision": "Accept Option A",
        "Safety_Override": "No",
        "Planned_Stop_Min": 15,
        "Unplanned_Downtime_Min": 150.0,
        "OptionA_Total_PKR": 47500,
        "OptionB_Total_PKR": 777000.0,
        "Net_Avoided_Loss_PKR": 729500.0,
        "Production_Hours_Rescued": 2.250000,
        "Notes": "Preventive intervention approved after Option A vs Option B cost comparison.",
    },
    {
        "Event_Date": "2026-08-22",
        "Month_Key": "2026-08",
        "Machine_ID": "M-202",
        "Error_ID": "M2-E03",
        "Stage": 2,
        "Failure_Category": "Mechanical",
        "Failure_Mode": "Pump Cavitation",
        "Reported_By": "Imran P.",
        "Shift": "A",
        "Decision": "Accept Option A",
        "Safety_Override": "No",
        "Planned_Stop_Min": 10,
        "Unplanned_Downtime_Min": 110.0,
        "OptionA_Total_PKR": 28000,
        "OptionB_Total_PKR": 441800.0,
        "Net_Avoided_Loss_PKR": 413800.0,
        "Production_Hours_Rescued": 1.666667,
        "Notes": "Preventive intervention approved after Option A vs Option B cost comparison.",
    },
    {
        "Event_Date": "2026-08-28",
        "Month_Key": "2026-08",
        "Machine_ID": "M-202",
        "Error_ID": "M2-E05",
        "Stage": 2,
        "Failure_Category": "Safety",
        "Failure_Mode": "Enclosure Interlock Fault",
        "Reported_By": "Imran P.",
        "Shift": "B",
        "Decision": "Mandatory Stop",
        "Safety_Override": "Yes",
        "Planned_Stop_Min": 10,
        "Unplanned_Downtime_Min": 0.0,
        "OptionA_Total_PKR": 31500,
        "OptionB_Total_PKR": 0.0,
        "Net_Avoided_Loss_PKR": 0.0,
        "Production_Hours_Rescued": 0.0,
        "Notes": "Safety-critical condition. Economic deferral prohibited; immediate intervention enforced.",
    },
    {
        "Event_Date": "2026-09-02",
        "Month_Key": "2026-09",
        "Machine_ID": "M-101",
        "Error_ID": "M1-E02",
        "Stage": 1,
        "Failure_Category": "Electrical",
        "Failure_Mode": "Motor Terminal Overheating",
        "Reported_By": "Tariq M.",
        "Shift": "A",
        "Decision": "Accept Option A",
        "Safety_Override": "No",
        "Planned_Stop_Min": 10,
        "Unplanned_Downtime_Min": 120.0,
        "OptionA_Total_PKR": 36500,
        "OptionB_Total_PKR": 622000.0,
        "Net_Avoided_Loss_PKR": 585500.0,
        "Production_Hours_Rescued": 1.833333,
        "Notes": "Preventive intervention approved after Option A vs Option B cost comparison.",
    },
    {
        "Event_Date": "2026-09-05",
        "Month_Key": "2026-09",
        "Machine_ID": "M-101",
        "Error_ID": "M1-E02",
        "Stage": 1,
        "Failure_Category": "Electrical",
        "Failure_Mode": "Motor Terminal Overheating",
        "Reported_By": "Kashif R.",
        "Shift": "B",
        "Decision": "Accept Option A",
        "Safety_Override": "No",
        "Planned_Stop_Min": 10,
        "Unplanned_Downtime_Min": 120.0,
        "OptionA_Total_PKR": 36500,
        "OptionB_Total_PKR": 622000.0,
        "Net_Avoided_Loss_PKR": 585500.0,
        "Production_Hours_Rescued": 1.833333,
        "Notes": "Preventive intervention approved after Option A vs Option B cost comparison.",
    },
    {
        "Event_Date": "2026-09-08",
        "Month_Key": "2026-09",
        "Machine_ID": "M-201",
        "Error_ID": "M2-E04",
        "Stage": 2,
        "Failure_Category": "Electrical",
        "Failure_Mode": "Solenoid Overheating",
        "Reported_By": "Salman A.",
        "Shift": "A",
        "Decision": "Accept Option A",
        "Safety_Override": "No",
        "Planned_Stop_Min": 10,
        "Unplanned_Downtime_Min": 140.0,
        "OptionA_Total_PKR": 30000,
        "OptionB_Total_PKR": 781200.0,
        "Net_Avoided_Loss_PKR": 751200.0,
        "Production_Hours_Rescued": 2.166667,
        "Notes": "Preventive intervention approved after Option A vs Option B cost comparison.",
    },
    {
        "Event_Date": "2026-09-10",
        "Month_Key": "2026-09",
        "Machine_ID": "M-304",
        "Error_ID": "M3-E05",
        "Stage": 3,
        "Failure_Category": "Safety",
        "Failure_Mode": "E-Stop Ground Fault",
        "Reported_By": "Bilal N.",
        "Shift": "C",
        "Decision": "Mandatory Stop",
        "Safety_Override": "Yes",
        "Planned_Stop_Min": 10,
        "Unplanned_Downtime_Min": 0.0,
        "OptionA_Total_PKR": 16000,
        "OptionB_Total_PKR": 0.0,
        "Net_Avoided_Loss_PKR": 0.0,
        "Production_Hours_Rescued": 0.0,
        "Notes": "Safety-critical condition. Economic deferral prohibited; immediate intervention enforced.",
    },
]

@st.cache_data
def load_master_data():
    """Load asset registry and error matrix with fallback support."""
    excel_path = "factory_data.xlsx"
    assets_df = None
    errors_df = None
    history_df = None

    if os.path.exists(excel_path):
        try:
            assets_df = pd.read_excel(excel_path, sheet_name="Assets")
            errors_df = pd.read_excel(excel_path, sheet_name="Error_Matrix")
            history_df = pd.read_excel(excel_path, sheet_name="Historical_Events")
        except Exception:
            pass

    if assets_df is None or assets_df.empty:
        assets_df = pd.DataFrame(FALLBACK_ASSETS)
    if errors_df is None or errors_df.empty:
        errors_df = pd.DataFrame(FALLBACK_ERROR_MATRIX)
    if history_df is None or history_df.empty:
        history_df = pd.DataFrame(FALLBACK_HISTORICAL_EVENTS)

    numeric_cols_errors = [
        "Line_Loss_Rate_PKR_hr",
        "Planned_Downtime_min",
        "Planned_Production_Loss_PKR",
        "OptionA_Part_Cost_PKR",
        "OptionA_Labor_Cost_PKR",
        "OptionA_Total_PKR",
        "Unplanned_Downtime_min",
        "Unplanned_Production_Loss_PKR",
        "OptionB_Replacement_Cost_PKR",
        "OptionB_Freight_PKR",
        "OptionB_Idle_Operator_Cost_PKR",
        "OptionB_Emergency_Tech_Cost_PKR",
        "OptionB_Scrap_Cost_PKR",
        "OptionB_Total_PKR",
        "Net_Avoided_Loss_PKR",
    ]
    for col in numeric_cols_errors:
        if col in errors_df.columns:
            errors_df[col] = pd.to_numeric(errors_df[col], errors="coerce")

    return assets_df, errors_df, history_df

assets_df, errors_df, history_df = load_master_data()

# -----------------------------------------------------------------------------
# 3. SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "current_screen" not in st.session_state:
    st.session_state.current_screen = "dashboard"

if "eval_mode" not in st.session_state:
    st.session_state.eval_mode = "topology"

if "active_fault_machine" not in st.session_state:
    st.session_state.active_fault_machine = None

if "selected_machine" not in st.session_state:
    st.session_state.selected_machine = "M-101"

if "selected_error_id" not in st.session_state:
    st.session_state.selected_error_id = "M1-E01"

if "last_rectified" not in st.session_state:
    st.session_state.last_rectified = None

if "last_rectified_savings" not in st.session_state:
    st.session_state.last_rectified_savings = 0.0

if "history_log" not in st.session_state:
    initial_records = history_df.to_dict(orient="records")
    st.session_state.history_log = initial_records

if "monthly_summary" not in st.session_state:
    st.session_state.monthly_summary = {
        "2026-01": {"planned": 145000.0, "exposure": 2650000.0, "net": 2505000.0, "hours": 8.5},
        "2026-02": {"planned": 160000.0, "exposure": 2890000.0, "net": 2730000.0, "hours": 9.2},
        "2026-03": {"planned": 210000.0, "exposure": 3450000.0, "net": 3240000.0, "hours": 11.0},
        "2026-04": {"planned": 175000.0, "exposure": 2980000.0, "net": 2805000.0, "hours": 9.5},
        "2026-05": {"planned": 225000.0, "exposure": 3620000.0, "net": 3395000.0, "hours": 11.8},
        "2026-06": {"planned": 195000.0, "exposure": 3150000.0, "net": 2955000.0, "hours": 10.1},
        "2026-07": {"planned": 181750.0, "exposure": 3125500.0, "net": 2943750.0, "hours": 10.0},
        "2026-08": {"planned": 249500.0, "exposure": 3803800.0, "net": 3554300.0, "hours": 10.67},
        "2026-09": {"planned": 103000.0, "exposure": 2025200.0, "net": 1922200.0, "hours": 5.83},
        "2026-10": {"planned": 185000.0, "exposure": 3100000.0, "net": 2915000.0, "hours": 9.5},
        "2026-11": {"planned": 190000.0, "exposure": 3250000.0, "net": 3060000.0, "hours": 10.0},
        "2026-12": {"planned": 215000.0, "exposure": 3500000.0, "net": 3285000.0, "hours": 11.0},
    }

if "kpi_totals" not in st.session_state:
    st.session_state.kpi_totals = {
        "net_loss_avoided": sum(st.session_state.monthly_summary[k]["net"] for k in ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"]),
        "hours_rescued": sum(st.session_state.monthly_summary[k]["hours"] for k in ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"]),
        "stops_approved": 38,
        "safety_overrides": 9,
    }

if "defer_remark" not in st.session_state:
    st.session_state.defer_remark = ""

# -----------------------------------------------------------------------------
# 4. MASTER DATA ACCESSORS & TOPOLOGY FLOW CALCULATOR
# -----------------------------------------------------------------------------
def get_machine_meta(machine_id):
    row = assets_df[assets_df["Machine_ID"] == machine_id]
    if not row.empty:
        return row.iloc[0].to_dict()
    return FALLBACK_ASSETS[0]

def get_machine_errors(machine_id):
    matches = errors_df[errors_df["Applicable_Machines"].astype(str).str.contains(machine_id, na=False)]
    if matches.empty:
        meta = get_machine_meta(machine_id)
        stage = meta.get("Stage", 1)
        matches = errors_df[errors_df["Stage"] == stage]
    return matches

def get_topology_flow_state(active_fault_m):
    """
    Computes exact throughputs and pipeline states across the 1 -> 2 -> 4 tree.
    When active_fault_m is None, ALL 7 machines are RUNNING at 100% capacity (100 pkts/hr total).
    When a machine has an active fault, that line halts (0 pkts/hr), and
    downstream starve conditions propagate.
    """
    state = {
        "M-101": {"status": "RUNNING", "rate": 100, "pill": "status-pill-green", "text": "● 100 pkts/hr"},
        "M-201": {"status": "RUNNING", "rate": 50, "pill": "status-pill-green", "text": "● 50 pkts/hr"},
        "M-202": {"status": "RUNNING", "rate": 50, "pill": "status-pill-green", "text": "● 50 pkts/hr"},
        "M-301": {"status": "RUNNING", "rate": 25, "pill": "status-pill-green", "text": "● 25 pkts/hr"},
        "M-302": {"status": "RUNNING", "rate": 25, "pill": "status-pill-green", "text": "● 25 pkts/hr"},
        "M-303": {"status": "RUNNING", "rate": 25, "pill": "status-pill-green", "text": "● 25 pkts/hr"},
        "M-304": {"status": "RUNNING", "rate": 25, "pill": "status-pill-green", "text": "● 25 pkts/hr"},
        "pipes": {
            "m101_to_m201": "flow-line-moving",
            "m101_to_m202": "flow-line-moving",
            "m201_to_m301": "flow-line-moving",
            "m201_to_m302": "flow-line-moving",
            "m202_to_m303": "flow-line-moving",
            "m202_to_m304": "flow-line-moving",
        },
        "total_output": 100,
        "loss_pct": 0,
    }

    if not active_fault_m:
        return state

    if active_fault_m == "M-101":
        state["M-101"] = {"status": "HALTED", "rate": 0, "pill": "status-pill-red", "text": "⛔ HALTED (0 pkts/hr)"}
        for m in ["M-201", "M-202"]:
            state[m] = {"status": "STARVED", "rate": 0, "pill": "status-pill-amber", "text": "⚠️ STARVED (0 pkts/hr)"}
        for m in ["M-301", "M-302", "M-303", "M-304"]:
            state[m] = {"status": "STARVED", "rate": 0, "pill": "status-pill-amber", "text": "⚠️ STARVED (0 pkts/hr)"}
        for p in state["pipes"]:
            state["pipes"][p] = "flow-line-stopped"
        state["total_output"] = 0
        state["loss_pct"] = 100

    elif active_fault_m == "M-201":
        state["M-201"] = {"status": "HALTED", "rate": 0, "pill": "status-pill-red", "text": "⛔ HALTED (0 pkts/hr)"}
        state["M-301"] = {"status": "STARVED", "rate": 0, "pill": "status-pill-amber", "text": "⚠️ STARVED (0 pkts/hr)"}
        state["M-302"] = {"status": "STARVED", "rate": 0, "pill": "status-pill-amber", "text": "⚠️ STARVED (0 pkts/hr)"}
        state["pipes"]["m101_to_m201"] = "flow-line-stopped"
        state["pipes"]["m201_to_m301"] = "flow-line-stopped"
        state["pipes"]["m201_to_m302"] = "flow-line-stopped"
        state["total_output"] = 50
        state["loss_pct"] = 50

    elif active_fault_m == "M-202":
        state["M-202"] = {"status": "HALTED", "rate": 0, "pill": "status-pill-red", "text": "⛔ HALTED (0 pkts/hr)"}
        state["M-303"] = {"status": "STARVED", "rate": 0, "pill": "status-pill-amber", "text": "⚠️ STARVED (0 pkts/hr)"}
        state["M-304"] = {"status": "STARVED", "rate": 0, "pill": "status-pill-amber", "text": "⚠️ STARVED (0 pkts/hr)"}
        state["pipes"]["m101_to_m202"] = "flow-line-stopped"
        state["pipes"]["m202_to_m303"] = "flow-line-stopped"
        state["pipes"]["m202_to_m304"] = "flow-line-stopped"
        state["total_output"] = 50
        state["loss_pct"] = 50

    elif active_fault_m in ["M-301", "M-302", "M-303", "M-304"]:
        state[active_fault_m] = {"status": "HALTED", "rate": 0, "pill": "status-pill-red", "text": "⛔ HALTED (0 pkts/hr)"}
        if active_fault_m == "M-301":
            state["pipes"]["m201_to_m301"] = "flow-line-stopped"
        elif active_fault_m == "M-302":
            state["pipes"]["m201_to_m302"] = "flow-line-stopped"
        elif active_fault_m == "M-303":
            state["pipes"]["m202_to_m303"] = "flow-line-stopped"
        elif active_fault_m == "M-304":
            state["pipes"]["m202_to_m304"] = "flow-line-stopped"
        state["total_output"] = 75
        state["loss_pct"] = 25

    return state

topo_state = get_topology_flow_state(st.session_state.active_fault_machine)

# -----------------------------------------------------------------------------
# SCREEN 1: EXECUTIVE DASHBOARD (HIGH-LEVEL DETAILS ONLY)
# -----------------------------------------------------------------------------
if st.session_state.current_screen == "dashboard":
    st.markdown(
        """
    <div class="simple-header">
        <h1>Factory Downtime & Maintenance Decision Intelligence</h1>
        <div class="header-subtitle">Translating Technical Machine Risk into Boardroom & Executive Economics</div>
        <div class="thesis-badge">
            <span>💡</span>
            <span>Core Thesis: "Stop for 10 minutes now or lose 2 hours later?"</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if st.session_state.last_rectified:
        st.markdown(
            f'<div style="background: #ECFDF5; border: 1.5px solid #10B981; border-radius: 8px; padding: 12px 18px; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between;">'
            f'<div><span style="font-weight: 700; color: #059669; font-size: 0.98rem;">🎉 Recent Rectification Executed: {st.session_state.last_rectified} Resumed!</span>'
            f'<div style="color: #047857; font-size: 0.82rem; margin-top: 2px;">Option A preventative micro-stoppage performed. Net capital saved: PKR {st.session_state.last_rectified_savings:,.0f}. Full factory flow restored to 100 pkts/hr.</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # 4 Top KPI Cards
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

    with col_kpi1:
        st.markdown(
            f"""
        <div class="kpi-container">
            <div class="kpi-label">Net Capital Losses Avoided</div>
            <div class="kpi-value" style="color: #059669;">PKR {st.session_state.kpi_totals['net_loss_avoided']:,.0f}</div>
            <div class="kpi-subtext" style="color: #047857;">▲ Direct unbudgeted loss mitigated</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col_kpi2:
        st.markdown(
            f"""
        <div class="kpi-container">
            <div class="kpi-label">Production Hours Rescued</div>
            <div class="kpi-value" style="color: #0284C7;">{st.session_state.kpi_totals['hours_rescued']:.1f} hrs</div>
            <div class="kpi-subtext" style="color: #0369A1;">▲ Across 7 factory work centers</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col_kpi3:
        st.markdown(
            f"""
        <div class="kpi-container">
            <div class="kpi-label">Preventative Stops Approved</div>
            <div class="kpi-value" style="color: #D97706;">{st.session_state.kpi_totals['stops_approved']} Actions</div>
            <div class="kpi-subtext" style="color: #B45309;">▲ Scheduled micro-stoppages</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col_kpi4:
        st.markdown(
            f"""
        <div class="kpi-container">
            <div class="kpi-label">Safety Overrides Enforced</div>
            <div class="kpi-value" style="color: #DC2626;">{st.session_state.kpi_totals['safety_overrides']} Lockouts</div>
            <div class="kpi-subtext" style="color: #B91C1C;">■ Zero statutory non-compliance</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # CALL TO ACTION BANNER & EVALUATION LAUNCH BUTTON
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background: #FFFFFF; border: 1.5px solid #0284C7; border-radius: 10px; padding: 18px 24px; box-shadow: 0 4px 16px rgba(2, 132, 199, 0.08); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px;">
            <div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #0F172A; display: flex; align-items: center; gap: 8px;">
                    <span>⚖️</span> <span>Real-Time Maintenance Decision Evaluation Engine</span>
                </div>
                <div style="color: #475569; font-size: 0.88rem; margin-top: 4px;">
                    Inspect machinery anomalies, assess throughput bottlenecks, and evaluate <b>Option A (Planned Stop)</b> vs. <b>Option B (Run to Fail)</b> financial economics.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
    if st.button("🚀 Proceed to Decision Evaluation", key="btn_go_to_eval", type="primary", use_container_width=True):
        st.session_state.current_screen = "mode_select"
        st.rerun()

    # FULL YEAR 2026 PLOTLY CHART (LIGHT THEME)
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    with st.container():
        st.markdown(
            """
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px 20px 8px 20px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div style="font-size: 1.05rem; font-weight: 700; color: #0F172A;">
                    📊 Full Year 2026 Executive Capital Dynamics: Intervention Spend vs. Avoided Breakdown Exposure
                </div>
                <div style="font-size: 0.76rem; color: #64748B; font-weight: 600;">
                    HISTORICAL ACTUALS (JAN–AUG) &bull; LIVE MTD (SEP) &bull; PREDICTIVE RISK MITIGATION (OCT–DEC)
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        months = [
            "Jan 26", "Feb 26", "Mar 26", "Apr 26", "May 26", "Jun 26",
            "Jul 26", "Aug 26", "Sep 26 (MTD)", "Oct 26 (Proj)", "Nov 26 (Proj)", "Dec 26 (Proj)"
        ]
        m_keys = [
            "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06",
            "2026-07", "2026-08", "2026-09", "2026-10", "2026-11", "2026-12"
        ]
        planned_costs = [st.session_state.monthly_summary[k]["planned"] for k in m_keys]
        exposure_avoided = [st.session_state.monthly_summary[k]["exposure"] for k in m_keys]
        net_savings = [st.session_state.monthly_summary[k]["net"] for k in m_keys]

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                name="Planned Intervention Cost (Option A Spend)",
                x=months,
                y=planned_costs,
                marker_color="#059669",
                marker_line_color="#10B981",
                marker_line_width=1.2,
                hovertemplate="<b>%{x}</b><br>Planned Intervention Cost: PKR %{y:,.0f}<extra></extra>",
            )
        )

        fig.add_trace(
            go.Bar(
                name="Avoided Breakdown Exposure (Option B Exposure)",
                x=months,
                y=exposure_avoided,
                marker_color="#DC2626",
                marker_line_color="#EF4444",
                marker_line_width=1.2,
                hovertemplate="<b>%{x}</b><br>Avoided Breakdown Exposure: PKR %{y:,.0f}<extra></extra>",
            )
        )

        fig.add_trace(
            go.Scatter(
                name="Net Capital Losses Avoided",
                x=months,
                y=net_savings,
                mode="lines+markers",
                line=dict(color="#0284C7", width=2.8),
                marker=dict(size=7, color="#0284C7", symbol="circle"),
                hovertemplate="<b>%{x}</b><br>Net Capital Avoided: PKR %{y:,.0f}<extra></extra>",
            )
        )

        fig.update_layout(
            template="plotly_white",
            barmode="group",
            bargap=0.28,
            bargroupgap=0.08,
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            height=330,
            margin=dict(l=40, r=40, t=25, b=30),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(size=11, color="#334155", family="Segoe UI, Inter, sans-serif"),
            ),
            yaxis=dict(
                title=dict(text="Capital Impact (PKR)", font=dict(size=11, color="#64748B")),
                tickprefix="PKR ",
                tickformat="~s",
                gridcolor="#F1F5F9",
                zerolinecolor="#E2E8F0",
                tickfont=dict(size=11, color="#475569", family="Segoe UI, Inter, sans-serif"),
            ),
            xaxis=dict(
                tickfont=dict(size=11, color="#334155", family="Segoe UI, Inter, sans-serif"),
                gridcolor="#F1F5F9",
            ),
            font=dict(family="Segoe UI, Inter, sans-serif"),
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})



# -----------------------------------------------------------------------------
# SCREEN 2: EVALUATION MODE SELECTOR
# -----------------------------------------------------------------------------
elif st.session_state.current_screen == "mode_select":
    col_back, _ = st.columns([1.5, 3.5])
    with col_back:
        if st.button("⬅ Back to Executive Dashboard", key="btn_back_dash_from_mode", use_container_width=True):
            st.session_state.current_screen = "dashboard"
            st.rerun()

    st.markdown(
        """
        <div style="text-align: center; margin: 15px 0 30px 0;">
            <div style="display: inline-flex; align-items: center; gap: 8px; background: #E0F2FE; color: #0284C7; font-weight: 700; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.8px; padding: 4px 14px; border-radius: 20px; margin-bottom: 12px;">
                STEP 2 OF 3: SELECT INTERFACE
            </div>
            <h2 style="font-size: 1.85rem; font-weight: 800; color: #0F172A; margin: 0;">Choose Evaluation Interface</h2>
            <p style="color: #64748B; font-size: 0.95rem; max-width: 620px; margin: 8px auto 0 auto; line-height: 1.5;">
                Select how you would like to inspect plant machinery, diagnose failure scenarios, and evaluate financial decision trade-offs.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_mode1, col_mode2 = st.columns(2)

    with col_mode1:
        st.markdown(
            """
            <div class="mode-select-card">
                <div class="mode-card-icon">🏭</div>
                <div class="mode-card-title">Graphical Factory Topology</div>
                <div class="mode-card-desc">
                    Interactive <b>1 ➔ 2 ➔ 4 visual equipment layout</b> with live animated conveyor pipelines, equipment photographs, and dynamic trip/starvation propagation across all 7 work centers.
                </div>
                <div style="margin-bottom: 18px; font-size: 0.84rem; color: #475569; line-height: 1.6;">
                    <div>✔ Real-time animated conveyor pipelines</div>
                    <div>✔ Visual 1 ➔ 2 ➔ 4 flow & starvation tree</div>
                    <div>✔ Direct machine click-to-diagnose triggers</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("🏭 Launch Graphical Topology", key="btn_select_topo", type="primary", use_container_width=True):
            st.session_state.eval_mode = "topology"
            st.session_state.current_screen = "evaluation"
            st.rerun()

    with col_mode2:
        st.markdown(
            """
            <div class="mode-select-card">
                <div class="mode-card-icon">📋</div>
                <div class="mode-card-title">Direct Machine & Fault Dropdown</div>
                <div class="mode-card-desc">
                    Fast tabular selectbox registry to directly choose any equipment ID and failure symptom from standard dropdown menus for rapid technical diagnostic evaluations.
                </div>
                <div style="margin-bottom: 18px; font-size: 0.84rem; color: #475569; line-height: 1.6;">
                    <div>✔ Compact selectbox dropdown navigation</div>
                    <div>✔ Searchable equipment ID & failure symptom codes</div>
                    <div>✔ Fast streamlined keyboard-friendly entry</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("📋 Launch Dropdown Selector", key="btn_select_dropdown", type="primary", use_container_width=True):
            st.session_state.eval_mode = "dropdown"
            st.session_state.current_screen = "evaluation"
            st.rerun()

# -----------------------------------------------------------------------------
# SCREEN 3: OPERATIONAL DECISION WORKSPACE
# -----------------------------------------------------------------------------
elif st.session_state.current_screen == "evaluation":
    # 1. Top Navigation Bar
    nav_col1, nav_col2 = st.columns([1, 1])
    with nav_col1:
        if st.button("⬅ Back to Executive Dashboard", key="btn_back_dash_from_eval", use_container_width=True):
            st.session_state.current_screen = "dashboard"
            st.rerun()
    with nav_col2:
        mode_btn_text = "📋 Switch to Dropdown Mode" if st.session_state.eval_mode == "topology" else "🏭 Switch to Topology Mode"
        if st.button(mode_btn_text, key="btn_switch_mode_inline", use_container_width=True):
            st.session_state.eval_mode = "dropdown" if st.session_state.eval_mode == "topology" else "topology"
            st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 2. RENDER SELECTED EVALUATION MODE
    if st.session_state.eval_mode == "topology":
        st.markdown(
            """<div class="section-card">
<div class="section-title">
<span>🏭 Interactive 1 ➔ 2 ➔ 4 Factory Topology with Animated Conveyor Pipelines</span>
<span style="font-size: 0.8rem; font-weight: 400; color: #64748B; margin-left: auto;">
Operational flow animation reflects real-time machine trip &amp; starvation states
</span>
</div>""",
            unsafe_allow_html=True,
        )

        # Operational status & recovery button
        col_topo_hdr1, col_topo_hdr2 = st.columns([3.2, 1.2])
        with col_topo_hdr1:
            if st.session_state.active_fault_machine is None:
                st.markdown(
                    '<div style="background: #ECFDF5; border: 1px solid #10B981; border-radius: 8px; padding: 10px 16px; display: flex; align-items: center; gap: 10px;">'
                    '<span style="font-size: 1.2rem;">🟢</span>'
                    '<div><span style="font-weight: 700; color: #059669; font-size: 0.92rem;">All 7 Work Centers Operating Normally (100 pkts/hr)</span>'
                    '<div style="color: #475569; font-size: 0.78rem;">Click "⚡ Trigger / Inspect Fault" on any asset below to simulate failure modes and evaluate financial decision intelligence.</div></div>'
                    '</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div style="background: #FEF2F2; border: 1px solid #EF4444; border-radius: 8px; padding: 10px 16px; display: flex; align-items: center; gap: 10px;">'
                    f'<span style="font-size: 1.2rem;">⛔</span>'
                    f'<div><span style="font-weight: 700; color: #DC2626; font-size: 0.92rem;">Active Stoppage Simulated on {st.session_state.active_fault_machine} — Downstream Lines Starved</span>'
                    f'<div style="color: #475569; font-size: 0.78rem;">Review Option A vs Option B decision below, or click Resume to restore full throughput.</div></div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        with col_topo_hdr2:
            if st.button("▶️ Resume Normal Operation", key="btn_reset_all_topo", use_container_width=True):
                st.session_state.active_fault_machine = None
                st.session_state.last_rectified = None
                st.rerun()

        if st.session_state.last_rectified:
            st.markdown(
                f'<div style="background: #ECFDF5; border: 1.5px solid #10B981; border-radius: 8px; padding: 12px 18px; margin: 12px 0; display: flex; align-items: center; justify-content: space-between;">'
                f'<div><span style="font-weight: 700; color: #059669; font-size: 0.98rem;">🎉 Rectification Successfully Executed: {st.session_state.last_rectified} Resumed!</span>'
                f'<div style="color: #047857; font-size: 0.82rem; margin-top: 2px;">Option A preventative micro-stoppage performed. Net capital saved: PKR {st.session_state.last_rectified_savings:,.0f}. Conveyor pipeline flow restored to 100 pkts/hr.</div></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        # STAGE 1: HYDRAULIC PRESS (CENTER)
        st.markdown(
            f'<div class="topo-stage-header">Stage 1: Primary Forming Feeder (100% Plant Trip Point) &nbsp;|&nbsp; Flow: {topo_state["M-101"]["rate"]} pkts/hr</div>',
            unsafe_allow_html=True,
        )

        m1_cols = st.columns([1.4, 3.2, 1.4])
        with m1_cols[1]:
            m101_fault = (st.session_state.active_fault_machine == "M-101")
            m101_class = "topo-node topo-node-halted" if m101_fault else ("topo-node topo-node-active" if st.session_state.selected_machine == "M-101" else "topo-node")
            m101_meta = get_machine_meta("M-101")
            m101_img_b64 = get_image_base64(MACHINE_IMAGES.get("M-101"))
            m101_img_tag = (
                f'<div class="machine-img-box"><img src="data:image/jpeg;base64,{m101_img_b64}" class="machine-img" style="height: 180px;"></div>'
                if m101_img_b64
                else ""
            )

            st.markdown(
                f'<div class="{m101_class}">'
                f'<div class="topo-node-title">'
                f'<span>M-101 · {m101_meta["Machine_Type"]}</span>'
                f'<span class="status-pill {topo_state["M-101"]["pill"]}">{topo_state["M-101"]["text"]}</span>'
                f'</div>'
                f'{m101_img_tag}'
                f'<div class="topo-node-desc"><b>Rate:</b> {topo_state["M-101"]["rate"]} pkts/hr | <b>Loss Impact:</b> PKR 180,000/hr (100% Loss If Tripped)</div>'
                f'<div class="topo-node-meta">👤 Operators: {m101_meta["Operator_Assignment"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if m101_fault:
                if st.button("⛔ Active Anomaly on M-101 (Review Decision)", key="btn_m101", type="primary", use_container_width=True):
                    st.session_state.selected_machine = "M-101"
                    st.rerun()
            else:
                if st.button("⚡ Trigger / Inspect Fault on M-101", key="btn_m101", use_container_width=True):
                    st.session_state.active_fault_machine = "M-101"
                    st.session_state.selected_machine = "M-101"
                    m_errs = get_machine_errors("M-101")
                    st.session_state.selected_error_id = m_errs.iloc[0]["Error_ID"]
                    st.session_state.last_rectified = None
                    st.rerun()

        # ANIMATED CONVEYOR SPLIT 1 -> 2 (SVG)
        p1 = topo_state["pipes"]["m101_to_m201"]
        p2 = topo_state["pipes"]["m101_to_m202"]
        dot_p1 = "#DC2626" if "stopped" in p1 else "#059669"
        dot_p2 = "#DC2626" if "stopped" in p2 else "#059669"

        st.markdown(
            f'<div style="text-align: center; margin: 4px 0 10px 0;">'
            f'<svg width="100%" height="70" viewBox="0 0 700 70" preserveAspectRatio="none" style="overflow: visible;">'
            f'<path d="M 350 0 L 350 25" class="conveyor-track" />'
            f'<path d="M 350 25 L 175 25 L 175 70" class="conveyor-track" />'
            f'<path d="M 350 25 L 525 25 L 525 70" class="conveyor-track" />'
            f'<path d="M 350 0 L 350 25 L 175 25 L 175 70" class="{p1}" />'
            f'<path d="M 350 0 L 350 25 L 525 25 L 525 70" class="{p2}" />'
            f'<circle cx="175" cy="65" r="5" fill="{dot_p1}" />'
            f'<circle cx="525" cy="65" r="5" fill="{dot_p2}" />'
            f'</svg>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # STAGE 2: CNC MILLS (2 COLUMNS)
        st.markdown(
            f'<div class="topo-stage-header">Stage 2: High-Speed Milling Split (Parallel 50% Streams) &nbsp;|&nbsp; Combined: {topo_state["M-201"]["rate"] + topo_state["M-202"]["rate"]} pkts/hr</div>',
            unsafe_allow_html=True,
        )
        m2_cols = st.columns(2)

        # M-201
        with m2_cols[0]:
            m201_fault = (st.session_state.active_fault_machine == "M-201")
            is_starved_201 = (topo_state["M-201"]["status"] == "STARVED")
            m201_class = "topo-node topo-node-halted" if m201_fault else ("topo-node topo-node-active" if is_starved_201 else "topo-node")
            m201_meta = get_machine_meta("M-201")
            m201_img_b64 = get_image_base64(MACHINE_IMAGES.get("M-201"))
            m201_img_tag = (
                f'<div class="machine-img-box"><img src="data:image/jpeg;base64,{m201_img_b64}" class="machine-img" style="height: 140px;"></div>'
                if m201_img_b64
                else ""
            )

            st.markdown(
                f'<div class="{m201_class}">'
                f'<div class="topo-node-title">'
                f'<span>M-201 · CNC Mill A</span>'
                f'<span class="status-pill {topo_state["M-201"]["pill"]}">{topo_state["M-201"]["text"]}</span>'
                f'</div>'
                f'{m201_img_tag}'
                f'<div class="topo-node-desc"><b>Rate:</b> {topo_state["M-201"]["rate"]} pkts/hr | <b>Loss Impact:</b> PKR 120,000/hr (Feeds Cells M-301 & M-302)</div>'
                f'<div class="topo-node-meta">👤 Operator: {m201_meta["Operator_Assignment"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if m201_fault:
                if st.button("⛔ Active Anomaly on M-201 (Review Decision)", key="btn_m201", type="primary", use_container_width=True):
                    st.session_state.selected_machine = "M-201"
                    st.rerun()
            else:
                if st.button("⚡ Trigger / Inspect Fault on M-201", key="btn_m201", use_container_width=True):
                    st.session_state.active_fault_machine = "M-201"
                    st.session_state.selected_machine = "M-201"
                    m_errs = get_machine_errors("M-201")
                    st.session_state.selected_error_id = m_errs.iloc[0]["Error_ID"]
                    st.session_state.last_rectified = None
                    st.rerun()

        # M-202
        with m2_cols[1]:
            m202_fault = (st.session_state.active_fault_machine == "M-202")
            is_starved_202 = (topo_state["M-202"]["status"] == "STARVED")
            m202_class = "topo-node topo-node-halted" if m202_fault else ("topo-node topo-node-active" if is_starved_202 else "topo-node")
            m202_meta = get_machine_meta("M-202")
            m202_img_b64 = get_image_base64(MACHINE_IMAGES.get("M-202"))
            m202_img_tag = (
                f'<div class="machine-img-box"><img src="data:image/jpeg;base64,{m202_img_b64}" class="machine-img" style="height: 140px;"></div>'
                if m202_img_b64
                else ""
            )

            st.markdown(
                f'<div class="{m202_class}">'
                f'<div class="topo-node-title">'
                f'<span>M-202 · CNC Mill B</span>'
                f'<span class="status-pill {topo_state["M-202"]["pill"]}">{topo_state["M-202"]["text"]}</span>'
                f'</div>'
                f'{m202_img_tag}'
                f'<div class="topo-node-desc"><b>Rate:</b> {topo_state["M-202"]["rate"]} pkts/hr | <b>Loss Impact:</b> PKR 120,000/hr (Feeds Cells M-303 & M-304)</div>'
                f'<div class="topo-node-meta">👤 Operator: {m202_meta["Operator_Assignment"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if m202_fault:
                if st.button("⛔ Active Anomaly on M-202 (Review Decision)", key="btn_m202", type="primary", use_container_width=True):
                    st.session_state.selected_machine = "M-202"
                    st.rerun()
            else:
                if st.button("⚡ Trigger / Inspect Fault on M-202", key="btn_m202", use_container_width=True):
                    st.session_state.active_fault_machine = "M-202"
                    st.session_state.selected_machine = "M-202"
                    m_errs = get_machine_errors("M-202")
                    st.session_state.selected_error_id = m_errs.iloc[0]["Error_ID"]
                    st.session_state.last_rectified = None
                    st.rerun()

        # ANIMATED CONVEYOR SPLIT 2 -> 4 (SVG)
        p201_301 = topo_state["pipes"]["m201_to_m301"]
        p201_302 = topo_state["pipes"]["m201_to_m302"]
        p202_303 = topo_state["pipes"]["m202_to_m303"]
        p202_304 = topo_state["pipes"]["m202_to_m304"]
        dot_301 = "#DC2626" if "stopped" in p201_301 else "#059669"
        dot_302 = "#DC2626" if "stopped" in p201_302 else "#059669"
        dot_303 = "#DC2626" if "stopped" in p202_303 else "#059669"
        dot_304 = "#DC2626" if "stopped" in p202_304 else "#059669"

        st.markdown(
            f'<div style="text-align: center; margin: 4px 0 10px 0;">'
            f'<svg width="100%" height="70" viewBox="0 0 800 70" preserveAspectRatio="none" style="overflow: visible;">'
            f'<path d="M 200 0 L 200 25 L 100 25 L 100 70" class="conveyor-track" />'
            f'<path d="M 200 25 L 300 25 L 300 70" class="conveyor-track" />'
            f'<path d="M 200 0 L 200 25 L 100 25 L 100 70" class="{p201_301}" />'
            f'<path d="M 200 25 L 300 25 L 300 70" class="{p201_302}" />'
            f'<path d="M 600 0 L 600 25 L 500 25 L 500 70" class="conveyor-track" />'
            f'<path d="M 600 25 L 700 25 L 700 70" class="conveyor-track" />'
            f'<path d="M 600 0 L 600 25 L 500 25 L 500 70" class="{p202_303}" />'
            f'<path d="M 600 25 L 700 25 L 700 70" class="{p202_304}" />'
            f'<circle cx="100" cy="65" r="5" fill="{dot_301}" />'
            f'<circle cx="300" cy="65" r="5" fill="{dot_302}" />'
            f'<circle cx="500" cy="65" r="5" fill="{dot_303}" />'
            f'<circle cx="700" cy="65" r="5" fill="{dot_304}" />'
            f'</svg>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # STAGE 3: PACKAGING CELLS (4 COLUMNS)
        st.markdown(
            f'<div class="topo-stage-header">Stage 3: Automated Packaging Quad Cells (25% Split per Station) &nbsp;|&nbsp; Combined: {sum(topo_state[m]["rate"] for m in ["M-301", "M-302", "M-303", "M-304"])} pkts/hr</div>',
            unsafe_allow_html=True,
        )
        m3_cols = st.columns(4)

        pkg_machines = ["M-301", "M-302", "M-303", "M-304"]
        for i, m_id in enumerate(pkg_machines):
            with m3_cols[i]:
                m_fault = (st.session_state.active_fault_machine == m_id)
                is_starved_pkg = (topo_state[m_id]["status"] == "STARVED")
                m_class = "topo-node topo-node-halted" if m_fault else ("topo-node topo-node-active" if is_starved_pkg else "topo-node")
                m_meta = get_machine_meta(m_id)
                pkg_img_b64 = get_image_base64(MACHINE_IMAGES.get(m_id))
                pkg_img_tag = (
                    f'<div class="machine-img-box"><img src="data:image/jpeg;base64,{pkg_img_b64}" class="machine-img" style="height: 100px;"></div>'
                    if pkg_img_b64
                    else ""
                )

                st.markdown(
                    f'<div class="{m_class}">'
                    f'<div class="topo-node-title">'
                    f'<span style="font-size: 0.95rem;">{m_id}</span>'
                    f'<span class="status-pill {topo_state[m_id]["pill"]}">{topo_state[m_id]["text"]}</span>'
                    f'</div>'
                    f'{pkg_img_tag}'
                    f'<div class="topo-node-desc" style="font-size: 0.76rem;"><b>Cap:</b> {topo_state[m_id]["rate"]} pkts/hr | <b>Loss:</b> PKR 45k/hr</div>'
                    f'<div class="topo-node-meta" style="font-size: 0.72rem;">👤 {m_meta["Operator_Assignment"].split(";")[0]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                if m_fault:
                    if st.button(f"⛔ Active on {m_id}", key=f"btn_{m_id}", type="primary", use_container_width=True):
                        st.session_state.selected_machine = m_id
                        st.rerun()
                else:
                    if st.button(f"⚡ Inspect {m_id}", key=f"btn_{m_id}", use_container_width=True):
                        st.session_state.active_fault_machine = m_id
                        st.session_state.selected_machine = m_id
                        m_errs = get_machine_errors(m_id)
                        st.session_state.selected_error_id = m_errs.iloc[0]["Error_ID"]
                        st.session_state.last_rectified = None
                        st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # MODE 2: DROPDOWN / MANUAL REGISTRY ENTRY
    else:
        st.markdown(
            """
        <div class="section-card">
            <div class="section-title">📋 Direct Machine & Fault Selection Registry</div>
        """,
            unsafe_allow_html=True,
        )

        sel_col1, sel_col2 = st.columns([1, 2])

        with sel_col1:
            machine_list = assets_df["Machine_ID"].tolist()
            curr_m_idx = machine_list.index(st.session_state.selected_machine) if st.session_state.selected_machine in machine_list else 0
            new_m = st.selectbox(
                "Select Machine ID:",
                machine_list,
                index=curr_m_idx,
                key="sb_machine",
            )
            if new_m != st.session_state.selected_machine:
                st.session_state.selected_machine = new_m
                m_errs = get_machine_errors(new_m)
                st.session_state.selected_error_id = m_errs.iloc[0]["Error_ID"]
                st.rerun()

        with sel_col2:
            m_errs = get_machine_errors(st.session_state.selected_machine)
            err_options = m_errs["Error_ID"].tolist()
            err_labels = [
                f"{row['Error_ID']} - {row['Failure_Mode']} ({'SAFETY CRITICAL' if row['Safety_Critical'] else row['Failure_Category']})"
                for _, row in m_errs.iterrows()
            ]
            curr_e_idx = err_options.index(st.session_state.selected_error_id) if st.session_state.selected_error_id in err_options else 0

            selected_label = st.selectbox(
                "Select Active Fault / Symptom:",
                err_labels,
                index=curr_e_idx,
                key="sb_fault",
            )
            chosen_err_id = err_options[err_labels.index(selected_label)]
            if chosen_err_id != st.session_state.selected_error_id:
                st.session_state.selected_error_id = chosen_err_id
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # 3. ACTIVE FAULT LIBRARY SELECTOR (HORIZONTAL PILL ROW)
    curr_machine_id = st.session_state.selected_machine
    machine_meta = get_machine_meta(curr_machine_id)
    avail_errors = get_machine_errors(curr_machine_id)

    st.markdown(
        f"""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px 20px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
        <div style="font-size: 0.88rem; font-weight: 700; color: #0284C7; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px;">
            Active Fault Library for {curr_machine_id} ({machine_meta['Machine_Type']}):
        </div>
    """,
        unsafe_allow_html=True,
    )

    err_cols = st.columns(len(avail_errors))
    for idx, (_, e_row) in enumerate(avail_errors.iterrows()):
        e_id = e_row["Error_ID"]
        is_selected = (e_id == st.session_state.selected_error_id)
        btn_label = f"⚡ {e_id}: {e_row['Failure_Mode']}"
        if e_row["Safety_Critical"]:
            btn_label = f"🛑 {e_id}: {e_row['Failure_Mode']} (SAFETY)"
        with err_cols[idx]:
            if st.button(
                btn_label,
                key=f"pill_err_{e_id}",
                type="primary" if is_selected else "secondary",
                use_container_width=True,
            ):
                st.session_state.selected_error_id = e_id
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Retrieve currently active error record
    active_error_match = errors_df[errors_df["Error_ID"] == st.session_state.selected_error_id]
    if active_error_match.empty:
        active_error = avail_errors.iloc[0].to_dict()
    else:
        active_error = active_error_match.iloc[0].to_dict()

    # 4. DIAGNOSTIC & FINANCIAL DECISION GATEKEEPER
    st.markdown(
        """
    <div class="section-card">
        <div class="section-title">
            <span>⚖️ Diagnostic & Financial Decision Gatekeeper</span>
            <span style="font-size: 0.82rem; font-weight: 400; color: #64748B; margin-left: auto;">
                Deterministic calculations evaluated strictly outside the LLM
            </span>
        </div>
    """,
        unsafe_allow_html=True,
    )

    is_safety = bool(active_error.get("Safety_Critical", False))
    badge_color = "status-pill-red" if is_safety else "status-pill-amber"
    badge_text = "SAFETY CRITICAL LOCKOUT" if is_safety else f"{active_error.get('Failure_Category', 'Mechanical').upper()} INTERVENTION REQUIRED"

    curr_img_b64 = get_image_base64(MACHINE_IMAGES.get(curr_machine_id))
    diag_thumb_tag = (
        f'<img src="data:image/jpeg;base64,{curr_img_b64}" style="width: 170px; height: 95px; object-fit: cover; border-radius: 6px; border: 1.5px solid #0284C7; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">'
        if curr_img_b64
        else ""
    )

    st.markdown(
        f"""
    <div class="diagnostic-header">
        <div>
            <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                <div class="diag-title">
                    Asset: <span style="color: #0284C7; font-weight: 700;">{curr_machine_id} · {machine_meta['Machine_Type']}</span>
                    &nbsp;|&nbsp; Fault Code: <span style="color: #D97706; font-weight: 700;">{active_error['Error_ID']}</span>
                    &nbsp;|&nbsp; <span style="color: #0F172A; font-weight: 700;">{active_error['Failure_Mode']}</span>
                </div>
                <div>
                    <span class="status-pill {badge_color}">{badge_text}</span>
                </div>
            </div>
            <div class="diag-meta">
                <b>Observed Symptom:</b> <i>"{active_error.get('Symptom', 'Degradation detected')}"</i><br>
                <b>Assigned Shift Operators:</b> {machine_meta['Operator_Assignment']} &nbsp;|&nbsp;
                <b>Line Loss Rate:</b> PKR {machine_meta['Line_Loss_Rate_PKR_hr']:,.0f}/hr ({machine_meta['Throughput_Loss_if_Trip_pct']}% capacity loss)
            </div>
        </div>
        <div>
            {diag_thumb_tag}
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # HARD SAFETY LOCKOUT BANNER
    if is_safety:
        st.markdown(
            f"""
        <div class="safety-alert-banner">
            <div class="safety-alert-title">
                <span>🛑 MANDATORY SAFETY OVERRIDE: STATUTORY SHUTDOWN ENFORCED</span>
            </div>
            <div class="safety-alert-body">
                <b>Statutory Code Violation (OSHA 1910.212 / IEC 62061 SIL-2/3):</b><br>
                {active_error.get('Safety_Message', 'Operating with compromised safety circuitry or disabled interlocks violates statutory machinery safety regulations.')}<br>
                <div style="margin-top: 8px; font-weight: 700; color: #991B1B;">
                    🔒 OPTION B (RUN-TO-FAILURE) IS STATUTORILY LOCKED OUT. Economic deferral is strictly prohibited under industrial compliance codes.
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    col_opt_a, col_opt_b = st.columns(2)

    # LEFT COLUMN: OPTION A (INTERVENE NOW)
    with col_opt_a:
        opt_a_mins = float(active_error.get("Planned_Downtime_min", 10))
        opt_a_lost_prod = float(active_error.get("Planned_Production_Loss_PKR", (opt_a_mins / 60.0) * machine_meta["Line_Loss_Rate_PKR_hr"]))
        opt_a_labor = float(active_error.get("OptionA_Labor_Cost_PKR", 2500))
        opt_a_part_cost = float(active_error.get("OptionA_Part_Cost_PKR", 5000))
        opt_a_part_desc = active_error.get("OptionA_Part_Description", "Consumable / Wear Part")
        opt_a_total = float(active_error.get("OptionA_Total_PKR", opt_a_lost_prod + opt_a_labor + opt_a_part_cost))

        st.markdown(
            f"""
        <div class="option-card option-a-card">
            <div class="option-header" style="color: #059669;">
                <span>Option A: Intervene Now</span>
                <span class="status-pill status-pill-green">Planned Preventative Stop</span>
            </div>
            <div class="cost-row">
                <span class="cost-label">⏱ Planned Stoppage Duration:</span>
                <span class="cost-value" style="color: #059669; font-weight: 700;">{opt_a_mins:.0f} mins ({(opt_a_mins/60.0):.2f} hrs)</span>
            </div>
            <div class="cost-row">
                <span class="cost-label">📉 Lost Production Capacity Cost:</span>
                <span class="cost-value">PKR {opt_a_lost_prod:,.0f}</span>
            </div>
            <div class="cost-row">
                <span class="cost-label">🔧 Standard Technician Labor:</span>
                <span class="cost-value">PKR {opt_a_labor:,.0f}</span>
            </div>
            <div class="cost-row">
                <span class="cost-label">📦 Wear Part ({opt_a_part_desc}):</span>
                <span class="cost-value">PKR {opt_a_part_cost:,.0f}</span>
            </div>
            <div class="cost-row" style="color: #64748B;">
                <span class="cost-label">🚫 Idle Standby Labor Surcharge:</span>
                <span class="cost-value">PKR 0 (Absorbed in Shift)</span>
            </div>
            <div class="cost-row" style="color: #64748B;">
                <span class="cost-label">🚫 Expedited Freight / Scrap Waste:</span>
                <span class="cost-value">PKR 0 (Zero Scrap)</span>
            </div>
            <div class="total-cost-box total-cost-box-a">
                <div class="total-cost-label" style="color: #047857;">Total Planned Intervention Spend</div>
                <div class="total-cost-value" style="color: #059669;">PKR {opt_a_total:,.0f}</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # RIGHT COLUMN: OPTION B (RUN TO FAIL)
    with col_opt_b:
        if is_safety:
            st.markdown(
                f"""
            <div class="option-card option-b-card option-b-locked">
                <div class="option-header" style="color: #64748B;">
                    <span>Option B: Run to Fail / Defer</span>
                    <span class="status-pill status-pill-red">LOCKED OUT</span>
                </div>
                <div style="text-align: center; padding: 40px 10px;">
                    <div style="font-size: 3.5rem; margin-bottom: 10px;">🔒</div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: #DC2626;">
                        STATUTORY SAFETY LOCKOUT
                    </div>
                    <p style="color: #64748B; font-size: 0.9rem; margin-top: 8px;">
                        Running with this fault violates ISO 13849-1 and statutory safety law.<br>
                        Cost modeling is disabled because this action is legally prohibited.
                    </p>
                </div>
                <div class="total-cost-box" style="background: #F8FAFC; border: 1px solid #CBD5E1;">
                    <div class="total-cost-label" style="color: #64748B;">Option B Financial Exposure</div>
                    <div class="total-cost-value" style="color: #DC2626;">PROHIBITED</div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            opt_b_mins = float(active_error.get("Unplanned_Downtime_min", 120))
            opt_b_lost_prod = float(active_error.get("Unplanned_Production_Loss_PKR", (opt_b_mins / 60.0) * machine_meta["Line_Loss_Rate_PKR_hr"]))
            opt_b_idle_labor = float(active_error.get("OptionB_Idle_Operator_Cost_PKR", 12000))
            opt_b_emerg_tech = float(active_error.get("OptionB_Emergency_Tech_Cost_PKR", 25000))
            opt_b_part_cost = float(active_error.get("OptionB_Replacement_Cost_PKR", 150000))
            opt_b_part_desc = active_error.get("OptionB_Replacement_Description", "Complete Core Sub-Assembly")
            opt_b_freight = float(active_error.get("OptionB_Freight_PKR", 25000))
            opt_b_scrap_cost = float(active_error.get("OptionB_Scrap_Cost_PKR", 20000))
            opt_b_scrap_desc = active_error.get("OptionB_Scrap_Description", "Part / Tool Scrap")
            opt_b_total = float(active_error.get("OptionB_Total_PKR", opt_b_lost_prod + opt_b_idle_labor + opt_b_emerg_tech + opt_b_part_cost + opt_b_freight + opt_b_scrap_cost))

            st.markdown(
                f"""
            <div class="option-card option-b-card">
                <div class="option-header" style="color: #DC2626;">
                    <span>Option B: Run to Fail / Repair Later</span>
                    <span class="status-pill status-pill-red">Catastrophic Breakdown</span>
                </div>
                <div class="cost-row">
                    <span class="cost-label">💥 Catastrophic Breakdown Downtime:</span>
                    <span class="cost-value" style="color: #DC2626; font-weight: 700;">{opt_b_mins:.0f} mins ({(opt_b_mins/60.0):.2f} hrs)</span>
                </div>
                <div class="cost-row">
                    <span class="cost-label">📉 Compounded Lost Production:</span>
                    <span class="cost-value">PKR {opt_b_lost_prod:,.0f}</span>
                </div>
                <div class="cost-row">
                    <span class="cost-label">👥 Idle Downstream Line Labor:</span>
                    <span class="cost-value">PKR {opt_b_idle_labor:,.0f}</span>
                </div>
                <div class="cost-row">
                    <span class="cost-label">🚨 Emergency Technician Callout:</span>
                    <span class="cost-value">PKR {opt_b_emerg_tech:,.0f}</span>
                </div>
                <div class="cost-row">
                    <span class="cost-label">⚙️ Replacement ({opt_b_part_desc}):</span>
                    <span class="cost-value">PKR {opt_b_part_cost:,.0f}</span>
                </div>
                <div class="cost-row">
                    <span class="cost-label">✈️ Express Air Freight Surcharge:</span>
                    <span class="cost-value">PKR {opt_b_freight:,.0f}</span>
                </div>
                <div class="cost-row">
                    <span class="cost-label">🗑️ Scrap Waste ({opt_b_scrap_desc}):</span>
                    <span class="cost-value">PKR {opt_b_scrap_cost:,.0f}</span>
                </div>
                <div class="total-cost-box total-cost-box-b">
                    <div class="total-cost-label" style="color: #991B1B;">Total Catastrophic Exposure</div>
                    <div class="total-cost-value" style="color: #DC2626;">PKR {opt_b_total:,.0f}</div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # NET DECISION METRIC BANNER
    if not is_safety:
        net_avoided_pkr = opt_b_total - opt_a_total
        hours_saved = (opt_b_mins - opt_a_mins) / 60.0
        cost_multiplier = opt_b_total / opt_a_total if opt_a_total > 0 else 0

        st.markdown(
            f"""
        <div class="net-decision-banner">
            <div>
                <div class="net-banner-title">✅ High-Leverage Intervention Justification</div>
                <div class="net-banner-sub">
                    Investing <b>{opt_a_mins:.0f} minutes</b> now prevents <b>{opt_b_mins:.0f} minutes</b> of unplanned factory breakdown.<br>
                    Catastrophic run-to-fail exposure is <b>{cost_multiplier:.1f}× more expensive</b> than preventative service.
                </div>
            </div>
            <div class="net-banner-metrics">
                <div>
                    <div class="net-metric-num">+PKR {net_avoided_pkr:,.0f}</div>
                    <div class="net-metric-lbl">Net Capital Losses Avoided</div>
                </div>
                <div>
                    <div class="net-metric-num" style="color: #0284C7;">+{hours_saved:.1f} hrs</div>
                    <div class="net-metric-lbl">Production Uptime Rescued</div>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # 5. OPERATOR EXECUTION PROTOCOL
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown("### 📋 Operator Execution & Handover Protocol")

    if is_safety:
        if st.button("🛑 Execute Immediate Safety Stop & Lockout", type="primary", use_container_width=True):
            new_event = {
                "Event_Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Month_Key": "2026-09",
                "Machine_ID": curr_machine_id,
                "Error_ID": active_error["Error_ID"],
                "Stage": machine_meta["Stage"],
                "Failure_Category": "Safety",
                "Failure_Mode": active_error["Failure_Mode"],
                "Reported_By": machine_meta["Operator_Assignment"].split("(")[0].strip(),
                "Shift": "A",
                "Decision": "Mandatory Safety Lockout",
                "Safety_Override": "Yes",
                "Planned_Stop_Min": opt_a_mins,
                "Unplanned_Downtime_Min": 0.0,
                "OptionA_Total_PKR": opt_a_total,
                "OptionB_Total_PKR": 0.0,
                "Net_Avoided_Loss_PKR": 0.0,
                "Production_Hours_Rescued": 0.0,
                "Notes": f"Statutory Safety Lockout enforced for {active_error['Failure_Mode']}. Prohibited Option B.",
            }
            st.session_state.history_log.insert(0, new_event)
            st.session_state.kpi_totals["safety_overrides"] += 1
            st.session_state.active_fault_machine = None
            st.session_state.last_rectified = curr_machine_id
            st.session_state.last_rectified_savings = 0.0
            st.toast(f"🛑 Statutory safety lockout executed for {curr_machine_id}. Safe isolation logged.", icon="🛑")
            st.rerun()

    else:
        action_col1, action_col2 = st.columns([1, 1])

        with action_col1:
            if st.button(
                f"✅ Accept Option A: Schedule Immediate Stoppage ({opt_a_mins:.0f} min)",
                type="primary",
                use_container_width=True,
            ):
                net_val = opt_b_total - opt_a_total
                rescued_hrs = (opt_b_mins - opt_a_mins) / 60.0

                new_event = {
                    "Event_Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Month_Key": "2026-09",
                    "Machine_ID": curr_machine_id,
                    "Error_ID": active_error["Error_ID"],
                    "Stage": machine_meta["Stage"],
                    "Failure_Category": active_error.get("Failure_Category", "Mechanical"),
                    "Failure_Mode": active_error["Failure_Mode"],
                    "Reported_By": machine_meta["Operator_Assignment"].split("(")[0].strip(),
                    "Shift": "A",
                    "Decision": "Accept Option A",
                    "Safety_Override": "No",
                    "Planned_Stop_Min": opt_a_mins,
                    "Unplanned_Downtime_Min": opt_b_mins,
                    "OptionA_Total_PKR": opt_a_total,
                    "OptionB_Total_PKR": opt_b_total,
                    "Net_Avoided_Loss_PKR": net_val,
                    "Production_Hours_Rescued": rescued_hrs,
                    "Notes": f"Preventative stop approved: Saved PKR {net_val:,.0f} and {rescued_hrs:.1f} hrs.",
                }
                st.session_state.history_log.insert(0, new_event)

                st.session_state.kpi_totals["net_loss_avoided"] += net_val
                st.session_state.kpi_totals["hours_rescued"] += rescued_hrs
                st.session_state.kpi_totals["stops_approved"] += 1

                st.session_state.monthly_summary["2026-09"]["planned"] += opt_a_total
                st.session_state.monthly_summary["2026-09"]["exposure"] += opt_b_total
                st.session_state.monthly_summary["2026-09"]["net"] += net_val
                st.session_state.monthly_summary["2026-09"]["hours"] += rescued_hrs

                # RESUME FULL PLANT OPERATIONS
                st.session_state.active_fault_machine = None
                st.session_state.last_rectified = curr_machine_id
                st.session_state.last_rectified_savings = net_val
                st.toast(f"✅ Option A Executed: {curr_machine_id} repaired! Normal factory flow resumed at 100 pkts/hr. PKR {net_val:,.0f} preserved!", icon="🎉")
                st.rerun()

        with action_col2:
            with st.expander("⚠️ Defer: Continue Running (Log Risk to Shift Handover)"):
                defer_reason = st.text_input(
                    "Mandatory Operational Justification for Deferral:",
                    placeholder="e.g. Critical customer shipment quota pending on current shift...",
                    key="input_defer_reason",
                )
                if st.button("Confirm Deferral & Register Exposure", type="secondary", use_container_width=True):
                    if not defer_reason.strip():
                        st.error("Operational justification is mandatory before logging a deferral.")
                    else:
                        new_event = {
                            "Event_Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "Month_Key": "2026-09",
                            "Machine_ID": curr_machine_id,
                            "Error_ID": active_error["Error_ID"],
                            "Stage": machine_meta["Stage"],
                            "Failure_Category": active_error.get("Failure_Category", "Mechanical"),
                            "Failure_Mode": active_error["Failure_Mode"],
                            "Reported_By": machine_meta["Operator_Assignment"].split("(")[0].strip(),
                            "Shift": "A",
                            "Decision": "Deferred (Run-to-Fail Risk)",
                            "Safety_Override": "No",
                            "Planned_Stop_Min": 0,
                            "Unplanned_Downtime_Min": opt_b_mins,
                            "OptionA_Total_PKR": 0.0,
                            "OptionB_Total_PKR": opt_b_total,
                            "Net_Avoided_Loss_PKR": -opt_b_total,
                            "Production_Hours_Rescued": 0.0,
                            "Notes": f"DEFERRED BY OPERATOR. Justification: {defer_reason.strip()}",
                        }
                        st.session_state.history_log.insert(0, new_event)
                        st.session_state.active_fault_machine = None
                        st.session_state.last_rectified = None
                        st.warning(f"⚠️ Deferral registered. Active exposure of PKR {opt_b_total:,.0f} logged to shift handover.")
                        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # 6. RETURN BUTTON AT BOTTOM OF SCREEN 3
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    if st.button("⬅ Return to Executive Dashboard", key="btn_bottom_back_dash", use_container_width=True):
        st.session_state.current_screen = "dashboard"
        st.rerun()

# -----------------------------------------------------------------------------
# 15. FOOTER
# -----------------------------------------------------------------------------
st.markdown(
    """
<div style="text-align: center; color: #64748B; font-size: 0.82rem; margin-top: 30px; padding: 20px 0; border-top: 1px solid #E2E8F0;">
    Industrial AI Hackathon • Cohort 11 Research Edition • Built with Streamlit & Plotly • Zero External LLM Math Dependencies
</div>
""",
    unsafe_allow_html=True,
)
