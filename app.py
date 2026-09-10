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

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & INLINE INDUSTRIAL DARK CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Maintenance Decision Intelligence",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for Industrial Dark Theme
st.markdown(
    """
<style>
    /* Dark Industrial Theme Palette */
    :root {
        --bg-main: #0E1117;
        --bg-card: #161B22;
        --bg-card-alt: #1E2433;
        --border-subtle: #30363D;
        --accent-blue: #1976D2;
        --accent-blue-light: #42A5F5;
        --emerald: #2E7D32;
        --emerald-bright: #4CAF50;
        --emerald-bg: rgba(46, 125, 50, 0.12);
        --crimson: #C62828;
        --crimson-bright: #EF5350;
        --crimson-bg: rgba(198, 40, 40, 0.12);
        --amber: #F57C00;
        --amber-bg: rgba(245, 124, 0, 0.12);
        --text-white: #F0F6FC;
        --text-muted: #8B949E;
        --font-mono: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
    }

    /* Overall page background */
    .stApp {
        background-color: var(--bg-main);
        color: var(--text-white);
    }

    /* Title & Banner Styling */
    .main-header {
        background: linear-gradient(135deg, #131720 0%, #1A2234 100%);
        border: 1px solid #30363D;
        border-left: 6px solid var(--accent-blue);
        border-radius: 8px;
        padding: 22px 28px;
        margin-bottom: 24px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    }
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .main-subtitle {
        font-size: 1.05rem;
        color: var(--text-muted);
        margin-top: 6px;
        font-weight: 400;
    }
    .thesis-tag {
        display: inline-block;
        background: rgba(25, 118, 210, 0.2);
        border: 1px solid var(--accent-blue);
        color: var(--accent-blue-light);
        font-size: 0.85rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 20px;
        margin-top: 10px;
        font-family: var(--font-mono);
    }

    /* Top KPI Metric Cards */
    .kpi-container {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 8px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .kpi-container:hover {
        border-color: var(--accent-blue);
        transform: translateY(-2px);
    }
    .kpi-label {
        font-size: 0.82rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 700;
        font-family: var(--font-mono);
        color: #FFFFFF;
        line-height: 1.2;
    }
    .kpi-subtext {
        font-size: 0.8rem;
        color: var(--emerald-bright);
        font-weight: 500;
        margin-top: 4px;
    }

    /* Section Cards */
    .section-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 24px;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.3);
    }
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
        border-bottom: 1px solid var(--border-subtle);
        padding-bottom: 10px;
    }

    /* Factory Topology Visual Nodes */
    .topo-stage-header {
        font-size: 0.88rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: var(--accent-blue-light);
        margin-bottom: 10px;
        text-align: center;
    }
    .topo-node {
        background: var(--bg-card-alt);
        border: 1px solid var(--border-subtle);
        border-radius: 8px;
        padding: 14px;
        text-align: left;
        transition: all 0.25s ease;
        position: relative;
    }
    .topo-node-active {
        border: 2px solid var(--accent-blue-light) !important;
        box-shadow: 0 0 16px rgba(66, 165, 245, 0.35);
        background: #1C273C !important;
    }
    .topo-node-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #FFFFFF;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .topo-node-desc {
        font-size: 0.82rem;
        color: var(--text-muted);
        margin-top: 4px;
    }
    .topo-node-meta {
        font-size: 0.78rem;
        color: #A0AEC0;
        margin-top: 8px;
        font-family: var(--font-mono);
    }
    .status-pill {
        display: inline-block;
        padding: 3px 9px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    .status-pill-green {
        background: var(--emerald-bg);
        color: var(--emerald-bright);
        border: 1px solid var(--emerald);
    }
    .status-pill-amber {
        background: var(--amber-bg);
        color: #FFB74D;
        border: 1px solid var(--amber);
    }
    .status-pill-red {
        background: var(--crimson-bg);
        color: var(--crimson-bright);
        border: 1px solid var(--crimson);
    }

    /* Pipeline Connector Flow Arrow */
    .pipe-connector {
        text-align: center;
        color: #4A5568;
        font-size: 1.4rem;
        font-weight: 900;
        margin: 6px 0;
        line-height: 1;
    }

    /* Decision Gatekeeper Side-by-Side Cards */
    .option-card {
        border-radius: 8px;
        padding: 22px;
        height: 100%;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    }
    .option-a-card {
        background: #111B15;
        border: 1.5px solid var(--emerald);
    }
    .option-b-card {
        background: #1F1315;
        border: 1.5px solid var(--crimson);
    }
    .option-b-locked {
        background: #16181C !important;
        border: 1.5px dashed #4A5568 !important;
        opacity: 0.45;
        filter: grayscale(80%);
    }
    .option-header {
        font-size: 1.25rem;
        font-weight: 700;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 10px;
    }
    .cost-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        font-size: 0.92rem;
    }
    .cost-label {
        color: #CBD5E0;
    }
    .cost-value {
        font-family: var(--font-mono);
        font-weight: 600;
        color: #FFFFFF;
    }
    .total-cost-box {
        margin-top: 18px;
        padding: 14px;
        border-radius: 6px;
        text-align: right;
    }
    .total-cost-box-a {
        background: rgba(46, 125, 50, 0.25);
        border: 1px solid var(--emerald-bright);
    }
    .total-cost-box-b {
        background: rgba(198, 40, 40, 0.25);
        border: 1px solid var(--crimson-bright);
    }
    .total-cost-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 600;
    }
    .total-cost-value {
        font-size: 2.1rem;
        font-weight: 800;
        font-family: var(--font-mono);
        line-height: 1.2;
    }

    /* Net Decision Banner */
    .net-decision-banner {
        background: linear-gradient(90deg, #102A1C 0%, #153A26 100%);
        border: 2px solid var(--emerald-bright);
        border-radius: 8px;
        padding: 20px 26px;
        margin: 20px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(46, 125, 50, 0.35);
    }
    .net-banner-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #FFFFFF;
    }
    .net-banner-sub {
        font-size: 0.9rem;
        color: #A7F3D0;
        margin-top: 4px;
    }
    .net-banner-metrics {
        display: flex;
        gap: 32px;
        text-align: right;
    }
    .net-metric-num {
        font-size: 2.1rem;
        font-weight: 800;
        font-family: var(--font-mono);
        color: #6EE7B7;
    }
    .net-metric-lbl {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #D1FAE5;
    }

    /* Statutory Safety Alert Banner */
    .safety-alert-banner {
        background: linear-gradient(90deg, #380C11 0%, #521219 100%);
        border: 2px solid var(--crimson-bright);
        border-radius: 8px;
        padding: 22px 28px;
        margin: 20px 0;
        box-shadow: 0 4px 24px rgba(239, 83, 80, 0.4);
    }
    .safety-alert-title {
        font-size: 1.35rem;
        font-weight: 800;
        color: #FFA4A2;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .safety-alert-body {
        font-size: 0.96rem;
        color: #FFCDD2;
        margin-top: 10px;
        line-height: 1.5;
    }

    /* Diagnostic Callout Header */
    .diagnostic-header {
        background: #1A202C;
        border: 1px solid var(--border-subtle);
        border-left: 4px solid var(--accent-blue);
        border-radius: 6px;
        padding: 14px 20px;
        margin-bottom: 18px;
    }
    .diag-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #FFFFFF;
    }
    .diag-meta {
        font-size: 0.88rem;
        color: var(--text-muted);
        margin-top: 4px;
    }

    /* Button Customization */
    div.stButton > button:first-child {
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.2s ease;
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

    # Clean and cast columns explicitly to numeric
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
if "selected_machine" not in st.session_state:
    st.session_state.selected_machine = "M-101"

if "selected_error_id" not in st.session_state:
    st.session_state.selected_error_id = "M1-E01"

if "nav_mode" not in st.session_state:
    st.session_state.nav_mode = "🏭 Graphical Factory Topology"

if "history_log" not in st.session_state:
    # Seed historical records
    initial_records = history_df.to_dict(orient="records")
    st.session_state.history_log = initial_records

if "monthly_summary" not in st.session_state:
    st.session_state.monthly_summary = {
        "2026-07": {"planned": 181750.0, "exposure": 3125500.0, "net": 2943750.0, "hours": 10.0},
        "2026-08": {"planned": 249500.0, "exposure": 3803800.0, "net": 3554300.0, "hours": 10.666667},
        "2026-09": {"planned": 103000.0, "exposure": 2025200.0, "net": 1922200.0, "hours": 5.833333},
    }

if "kpi_totals" not in st.session_state:
    st.session_state.kpi_totals = {
        "net_loss_avoided": 8420250.0,
        "hours_rescued": 26.5,
        "stops_approved": 11,
        "safety_overrides": 3,
    }

if "defer_remark" not in st.session_state:
    st.session_state.defer_remark = ""

# -----------------------------------------------------------------------------
# 4. TOP TITLE BANNER & EXECUTIVE SUMMARY
# -----------------------------------------------------------------------------
st.markdown(
    """
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
        <div>
            <h1 class="main-title">Factory Downtime & Maintenance Decision Intelligence</h1>
            <p class="main-subtitle">Translating Technical Machine Risk into Boardroom & Executive Economics</p>
            <div class="thesis-tag">💡 Core Operational Thesis: "Stop for 10 minutes now or lose 2 hours later?"</div>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 0.8rem; color: #8B949E; font-family: var(--font-mono); text-transform: uppercase;">Plant Operating Status</div>
            <div style="font-size: 1.1rem; color: #4CAF50; font-weight: 700; margin-top: 3px;">● 100 pkts/hr Balanced Topology</div>
            <div style="font-size: 0.82rem; color: #A0AEC0; margin-top: 4px;">Audit Window: July 2026 – September 2026 (Live)</div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 5. STRATEGIC SAVINGS DASHBOARD (JULY 2026 - MTD)
# -----------------------------------------------------------------------------
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    st.markdown(
        f"""
    <div class="kpi-container">
        <div class="kpi-label">Net Capital Losses Avoided</div>
        <div class="kpi-value" style="color: #4CAF50;">PKR {st.session_state.kpi_totals['net_loss_avoided']:,.0f}</div>
        <div class="kpi-subtext">▲ Direct unbudgeted loss mitigated</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_kpi2:
    st.markdown(
        f"""
    <div class="kpi-container">
        <div class="kpi-label">Production Hours Rescued</div>
        <div class="kpi-value" style="color: #42A5F5;">{st.session_state.kpi_totals['hours_rescued']:.1f} hrs</div>
        <div class="kpi-subtext">▲ Across 7 active work centers</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_kpi3:
    st.markdown(
        f"""
    <div class="kpi-container">
        <div class="kpi-label">Preventative Stops Approved</div>
        <div class="kpi-value" style="color: #FFB74D;">{st.session_state.kpi_totals['stops_approved']} Actions</div>
        <div class="kpi-subtext">▲ Scheduled micro-stoppages</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_kpi4:
    st.markdown(
        f"""
    <div class="kpi-container">
        <div class="kpi-label">Safety Overrides Enforced</div>
        <div class="kpi-value" style="color: #EF5350;">{st.session_state.kpi_totals['safety_overrides']} Lockouts</div>
        <div class="kpi-subtext" style="color: #EF5350;">■ Zero OSHA/IEC non-compliance</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. INTERACTIVE MONTHLY TREND CHART (PLOTLY GRAPH OBJECTS)
# -----------------------------------------------------------------------------
with st.container():
    st.markdown(
        """
    <div style="background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 18px 20px 8px 20px; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="font-size: 1.15rem; font-weight: 700; color: #FFFFFF;">
                📊 Executive Capital Preservation Dynamics: Intervention Spend vs. Avoided Breakdown Exposure
            </div>
            <div style="font-size: 0.8rem; color: #8B949E; font-family: var(--font-mono);">
                AUDITED HISTORICAL (JUL-AUG) + CURRENT CYCLE (SEP MTD)
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    months = ["July 2026", "August 2026", "September 2026 (MTD)"]
    m_keys = ["2026-07", "2026-08", "2026-09"]
    planned_costs = [st.session_state.monthly_summary[k]["planned"] for k in m_keys]
    exposure_avoided = [st.session_state.monthly_summary[k]["exposure"] for k in m_keys]
    net_savings = [st.session_state.monthly_summary[k]["net"] for k in m_keys]

    fig = go.Figure()

    # Planned Intervention Costs (Option A spend)
    fig.add_trace(
        go.Bar(
            name="Planned Intervention Cost (Option A Spend)",
            x=months,
            y=planned_costs,
            marker_color="#2E7D32",
            marker_line_color="#4CAF50",
            marker_line_width=1.5,
            hovertemplate="<b>%{x}</b><br>Planned Intervention Cost: PKR %{y:,.0f}<extra></extra>",
        )
    )

    # Avoided Breakdown Exposure (Option B losses prevented)
    fig.add_trace(
        go.Bar(
            name="Avoided Breakdown Exposure (Option B Exposure)",
            x=months,
            y=exposure_avoided,
            marker_color="#C62828",
            marker_line_color="#EF5350",
            marker_line_width=1.5,
            hovertemplate="<b>%{x}</b><br>Avoided Breakdown Exposure: PKR %{y:,.0f}<extra></extra>",
        )
    )

    # Net Avoided Loss Line
    fig.add_trace(
        go.Scatter(
            name="Net Capital Losses Avoided",
            x=months,
            y=net_savings,
            mode="lines+markers+text",
            line=dict(color="#00E676", width=3, dash="dot"),
            marker=dict(size=9, color="#00E676", symbol="diamond"),
            text=[f"+PKR {v/1000000:.2f}M" for v in net_savings],
            textposition="top center",
            textfont=dict(family="SFMono-Regular, Consolas, monospace", size=11, color="#A7F3D0"),
            hovertemplate="<b>%{x}</b><br>Net Preserved: PKR %{y:,.0f}<extra></extra>",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        barmode="group",
        bargap=0.25,
        bargroupgap=0.1,
        plot_bgcolor="#161B22",
        paper_bgcolor="#161B22",
        height=330,
        margin=dict(l=40, r=40, t=20, b=30),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color="#E2E8F0"),
        ),
        yaxis=dict(
            title=dict(text="Capital Impact (PKR)", font=dict(size=12, color="#94A3B8")),
            tickprefix="PKR ",
            tickformat=",",
            gridcolor="#2D3748",
            zerolinecolor="#4A5568",
        ),
        xaxis=dict(
            tickfont=dict(size=12, color="#E2E8F0"),
            gridcolor="#2D3748",
        ),
        font=dict(family="SFMono-Regular, Consolas, sans-serif"),
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# -----------------------------------------------------------------------------
# 7. DUAL NAVIGATION VIEW SWITCHER
# -----------------------------------------------------------------------------
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

nav_mode = st.radio(
    "Navigation Mode",
    ["🏭 Graphical Factory Topology", "📋 Dropdown / Manual Entry"],
    horizontal=True,
    index=0 if st.session_state.nav_mode == "🏭 Graphical Factory Topology" else 1,
    key="nav_mode_radio",
)
st.session_state.nav_mode = nav_mode

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

# -----------------------------------------------------------------------------
# 8. MODE 1: GRAPHICAL FACTORY TOPOLOGY (1 -> 2 -> 4 DIVERGING TREE)
# -----------------------------------------------------------------------------
if st.session_state.nav_mode == "🏭 Graphical Factory Topology":
    st.markdown(
        """
    <div class="section-card">
        <div class="section-title">
            <span>🏭 Balanced 1 ➔ 2 ➔ 4 Diverging Tree Factory Topology</span>
            <span style="font-size: 0.8rem; font-weight: 400; color: #8B949E; margin-left: auto;">
                Click [Inspect Asset / Select Fault] to evaluate economics in the Diagnostic Gatekeeper
            </span>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # --- STAGE 1: HYDRAULIC PRESS (CENTER) ---
    st.markdown('<div class="topo-stage-header">Stage 1: Primary Forming Feeder (Single Point of Failure • 100% Loss if Tripped)</div>', unsafe_allow_html=True)
    m1_cols = st.columns([1.5, 3, 1.5])
    with m1_cols[1]:
        m101_active = (st.session_state.selected_machine == "M-101")
        m101_class = "topo-node topo-node-active" if m101_active else "topo-node"
        m101_meta = get_machine_meta("M-101")
        st.markdown(
            f"""
        <div class="{m101_class}">
            <div class="topo-node-title">
                <span>M-101 · {m101_meta['Machine_Type']}</span>
                <span class="status-pill status-pill-amber">⚠ Fault Detected</span>
            </div>
            <div class="topo-node-desc"><b>Rate:</b> 100 pkts/hr | <b>Loss Impact:</b> PKR 180,000/hr (100% Plant Trip)</div>
            <div class="topo-node-meta">👤 Operators: {m101_meta['Operator_Assignment']}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button("🔍 Inspect M-101 Hydraulic Press", key="btn_m101", use_container_width=True):
            st.session_state.selected_machine = "M-101"
            m_errs = get_machine_errors("M-101")
            st.session_state.selected_error_id = m_errs.iloc[0]["Error_ID"]
            st.rerun()

    # Split Arrow 1 -> 2
    st.markdown(
        """
        <div class="pipe-connector">
            │<br>
            ┌───────────────┴───────────────┐<br>
            ▼                               ▼
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- STAGE 2: CNC MILLS (2 COLUMNS) ---
    st.markdown('<div class="topo-stage-header">Stage 2: High-Speed Milling Split (Parallel Split • 50% Loss if Tripped)</div>', unsafe_allow_html=True)
    m2_cols = st.columns(2)

    # M-201
    with m2_cols[0]:
        m201_active = (st.session_state.selected_machine == "M-201")
        m201_class = "topo-node topo-node-active" if m201_active else "topo-node"
        m201_meta = get_machine_meta("M-201")
        st.markdown(
            f"""
        <div class="{m201_class}">
            <div class="topo-node-title">
                <span>M-201 · CNC Mill A</span>
                <span class="status-pill status-pill-green">● Normal / Wear Check</span>
            </div>
            <div class="topo-node-desc"><b>Rate:</b> 50 pkts/hr | <b>Loss Impact:</b> PKR 120,000/hr (Downstream Cells Starve)</div>
            <div class="topo-node-meta">👤 Operator: {m201_meta['Operator_Assignment']}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button("🔍 Inspect M-201 CNC Mill A", key="btn_m201", use_container_width=True):
            st.session_state.selected_machine = "M-201"
            m_errs = get_machine_errors("M-201")
            st.session_state.selected_error_id = m_errs.iloc[0]["Error_ID"]
            st.rerun()

    # M-202
    with m2_cols[1]:
        m202_active = (st.session_state.selected_machine == "M-202")
        m202_class = "topo-node topo-node-active" if m202_active else "topo-node"
        m202_meta = get_machine_meta("M-202")
        st.markdown(
            f"""
        <div class="{m202_class}">
            <div class="topo-node-title">
                <span>M-202 · CNC Mill B</span>
                <span class="status-pill status-pill-green">● Normal / Wear Check</span>
            </div>
            <div class="topo-node-desc"><b>Rate:</b> 50 pkts/hr | <b>Loss Impact:</b> PKR 120,000/hr (Downstream Cells Starve)</div>
            <div class="topo-node-meta">👤 Operator: {m202_meta['Operator_Assignment']}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button("🔍 Inspect M-202 CNC Mill B", key="btn_m202", use_container_width=True):
            st.session_state.selected_machine = "M-202"
            m_errs = get_machine_errors("M-202")
            st.session_state.selected_error_id = m_errs.iloc[0]["Error_ID"]
            st.rerun()

    # Split Arrow 2 -> 4
    st.markdown(
        """
        <div class="pipe-connector" style="display: flex; justify-content: space-around;">
            <div>│<br>┌───────┴───────┐<br>▼               ▼</div>
            <div>│<br>┌───────┴───────┐<br>▼               ▼</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- STAGE 3: PACKAGING CELLS (4 COLUMNS) ---
    st.markdown('<div class="topo-stage-header">Stage 3: Automated Packaging Quad Cells (Quad Split • 25% Loss per Cell)</div>', unsafe_allow_html=True)
    m3_cols = st.columns(4)

    pkg_machines = ["M-301", "M-302", "M-303", "M-304"]
    for i, m_id in enumerate(pkg_machines):
        with m3_cols[i]:
            m_active = (st.session_state.selected_machine == m_id)
            m_class = "topo-node topo-node-active" if m_active else "topo-node"
            m_meta = get_machine_meta(m_id)
            st.markdown(
                f"""
            <div class="{m_class}">
                <div class="topo-node-title">
                    <span style="font-size: 0.95rem;">{m_id}</span>
                    <span class="status-pill status-pill-green">● Running</span>
                </div>
                <div class="topo-node-desc" style="font-size: 0.78rem;"><b>Cap:</b> 25 pkts/hr | <b>Loss:</b> PKR 45k/hr</div>
                <div class="topo-node-meta" style="font-size: 0.74rem;">👤 {m_meta['Operator_Assignment'].split(';')[0]}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
            if st.button(f"🔍 Inspect {m_id}", key=f"btn_{m_id}", use_container_width=True):
                st.session_state.selected_machine = m_id
                m_errs = get_machine_errors(m_id)
                st.session_state.selected_error_id = m_errs.iloc[0]["Error_ID"]
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 9. MODE 2: DROPDOWN / MANUAL ENTRY STYLE
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# 10. ACTIVE DIAGNOSTIC CONTEXT & FAULT SELECTOR (IF IN TOPOLOGY MODE)
# -----------------------------------------------------------------------------
curr_machine_id = st.session_state.selected_machine
machine_meta = get_machine_meta(curr_machine_id)
avail_errors = get_machine_errors(curr_machine_id)

if st.session_state.nav_mode == "🏭 Graphical Factory Topology":
    st.markdown(
        f"""
    <div style="background: #131722; border: 1px solid #2D3748; border-radius: 8px; padding: 14px 20px; margin-bottom: 20px;">
        <div style="font-size: 0.88rem; font-weight: 700; color: #90CDF4; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px;">
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

# -----------------------------------------------------------------------------
# 11. DIAGNOSTIC & FINANCIAL DECISION GATEKEEPER
# -----------------------------------------------------------------------------
st.markdown(
    """
<div class="section-card">
    <div class="section-title">
        <span>⚖️ Diagnostic & Financial Decision Gatekeeper</span>
        <span style="font-size: 0.82rem; font-weight: 400; color: #8B949E; margin-left: auto;">
            Deterministic calculations evaluated strictly outside the LLM
        </span>
    </div>
""",
    unsafe_allow_html=True,
)

is_safety = bool(active_error.get("Safety_Critical", False))
badge_color = "status-pill-red" if is_safety else "status-pill-amber"
badge_text = "SAFETY CRITICAL LOCKOUT" if is_safety else f"{active_error.get('Failure_Category', 'Mechanical').upper()} INTERVENTION REQUIRED"

st.markdown(
    f"""
<div class="diagnostic-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div class="diag-title">
            Asset: <span style="color: #60A5FA;">{curr_machine_id} · {machine_meta['Machine_Type']}</span>
            &nbsp;|&nbsp; Fault Code: <span style="color: #FCD34D;">{active_error['Error_ID']}</span>
            &nbsp;|&nbsp; <span style="color: #E2E8F0;">{active_error['Failure_Mode']}</span>
        </div>
        <div>
            <span class="status-pill {badge_color}">{badge_text}</span>
        </div>
    </div>
    <div class="diag-meta" style="margin-top: 8px;">
        <b>Observed Symptom:</b> <i>"{active_error.get('Symptom', 'Degradation detected')}"</i><br>
        <b>Assigned Shift Operators:</b> {machine_meta['Operator_Assignment']} &nbsp;|&nbsp;
        <b>Line Loss Rate:</b> PKR {machine_meta['Line_Loss_Rate_PKR_hr']:,.0f}/hr ({machine_meta['Throughput_Loss_if_Trip_pct']}% capacity loss)
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# --- HARD SAFETY & COMPLIANCE GATEKEEPER LOCKOUT ---
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
            <div style="margin-top: 10px; font-weight: 700; color: #FFFFFF;">
                🔒 OPTION B (RUN-TO-FAILURE) IS STATUTORILY LOCKED OUT. Economic deferral is strictly prohibited under industrial compliance codes.
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

col_opt_a, col_opt_b = st.columns(2)

# --- LEFT COLUMN: OPTION A (INTERVENE NOW) ---
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
        <div class="option-header" style="color: #4CAF50;">
            <span>Option A: Intervene Now</span>
            <span class="status-pill status-pill-green">Planned Preventative Stop</span>
        </div>
        <div class="cost-row">
            <span class="cost-label">⏱ Planned Stoppage Duration:</span>
            <span class="cost-value" style="color: #81C784;">{opt_a_mins:.0f} mins ({(opt_a_mins/60.0):.2f} hrs)</span>
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
            <div class="total-cost-label" style="color: #A7F3D0;">Total Planned Intervention Spend</div>
            <div class="total-cost-value" style="color: #4CAF50;">PKR {opt_a_total:,.0f}</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# --- RIGHT COLUMN: OPTION B (RUN TO FAIL / REPAIR LATER) ---
with col_opt_b:
    if is_safety:
        st.markdown(
            f"""
        <div class="option-card option-b-card option-b-locked">
            <div class="option-header" style="color: #94A3B8;">
                <span>Option B: Run to Fail / Defer</span>
                <span class="status-pill status-pill-red">LOCKED OUT</span>
            </div>
            <div style="text-align: center; padding: 40px 10px;">
                <div style="font-size: 3.5rem; margin-bottom: 10px;">🔒</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #EF5350;">
                    STATUTORY SAFETY LOCKOUT
                </div>
                <p style="color: #94A3B8; font-size: 0.9rem; margin-top: 8px;">
                    Running with this fault violates ISO 13849-1 and statutory safety law.<br>
                    Cost modeling is disabled because this action is legally prohibited.
                </p>
            </div>
            <div class="total-cost-box" style="background: rgba(45, 55, 72, 0.4); border: 1px solid #4A5568;">
                <div class="total-cost-label" style="color: #94A3B8;">Option B Financial Exposure</div>
                <div class="total-cost-value" style="color: #94A3B8;">PROHIBITED</div>
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
            <div class="option-header" style="color: #EF5350;">
                <span>Option B: Run to Fail / Repair Later</span>
                <span class="status-pill status-pill-red">Catastrophic Breakdown</span>
            </div>
            <div class="cost-row">
                <span class="cost-label">💥 Catastrophic Breakdown Downtime:</span>
                <span class="cost-value" style="color: #EF5350;">{opt_b_mins:.0f} mins ({(opt_b_mins/60.0):.2f} hrs)</span>
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
                <div class="total-cost-label" style="color: #FECDD3;">Total Catastrophic Exposure</div>
                <div class="total-cost-value" style="color: #EF5350;">PKR {opt_b_total:,.0f}</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

# --- NET DECISION METRIC BANNER ---
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
                <div class="net-metric-num">+{hours_saved:.1f} hrs</div>
                <div class="net-metric-lbl">Production Uptime Rescued</div>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# 12. OPERATOR ACTIONS & REAL-TIME AUDIT LOGGING
# -----------------------------------------------------------------------------
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
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
        st.toast("🛑 Statutory safety lockout executed and recorded into shift handover log.", icon="🛑")
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

            # Update KPI counters
            st.session_state.kpi_totals["net_loss_avoided"] += net_val
            st.session_state.kpi_totals["hours_rescued"] += rescued_hrs
            st.session_state.kpi_totals["stops_approved"] += 1

            # Update monthly totals
            st.session_state.monthly_summary["2026-09"]["planned"] += opt_a_total
            st.session_state.monthly_summary["2026-09"]["exposure"] += opt_b_total
            st.session_state.monthly_summary["2026-09"]["net"] += net_val
            st.session_state.monthly_summary["2026-09"]["hours"] += rescued_hrs

            st.toast(f"Intervention logged: PKR {net_val:,.0f} preserved!", icon="✅")
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
                    st.warning(f"⚠️ Deferral registered. Active exposure of PKR {opt_b_total:,.0f} logged to shift handover.")
                    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 13. AUDIT TRAIL & SHIFT HANDOVER LOG
# -----------------------------------------------------------------------------
st.markdown(
    """
<div class="section-card">
    <div class="section-title">
        <span>📜 Plant Shift Handover & Decision Audit Trail</span>
        <span style="font-size: 0.8rem; font-weight: 400; color: #8B949E; margin-left: auto;">
            Live immutable decision ledger (July 2026 – Date)
        </span>
    </div>
""",
    unsafe_allow_html=True,
)

audit_df = pd.DataFrame(st.session_state.history_log)

display_cols = [
    "Event_Date",
    "Machine_ID",
    "Error_ID",
    "Failure_Mode",
    "Reported_By",
    "Decision",
    "OptionA_Total_PKR",
    "OptionB_Total_PKR",
    "Net_Avoided_Loss_PKR",
    "Production_Hours_Rescued",
    "Notes",
]

valid_cols = [c for c in display_cols if c in audit_df.columns]
display_df = audit_df[valid_cols].copy()

st.dataframe(
    display_df.style.format(
        {
            "OptionA_Total_PKR": "PKR {:,.0f}",
            "OptionB_Total_PKR": "PKR {:,.0f}",
            "Net_Avoided_Loss_PKR": "PKR {:,.0f}",
            "Production_Hours_Rescued": "{:.1f} hrs",
        },
        na_rep="-",
    ),
    use_container_width=True,
    height=280,
)

csv_data = audit_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Export Shift Handover Audit Log (CSV)",
    data=csv_data,
    file_name=f"shift_handover_audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv",
)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 14. FOOTER
# -----------------------------------------------------------------------------
st.markdown(
    """
<div style="text-align: center; color: #64748B; font-size: 0.82rem; margin-top: 30px; padding: 20px 0; border-top: 1px solid #1E293B;">
    Industrial AI Hackathon • Cohort 11 Research Edition • Built with Streamlit & Plotly • Zero External LLM Math Dependencies
</div>
""",
    unsafe_allow_html=True,
)
