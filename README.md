# 🏭 Factory Downtime & Maintenance Decision Intelligence

> **"Stop for 10 minutes now or lose 2 hours later?"**  
> An explainable, deterministic maintenance economics decision-support system built for an industrial AI hackathon.

---

## Overview

In manufacturing facilities, preventive maintenance interventions are frequently delayed because the short-term disruption of stopping a running production line is immediately visible, while catastrophic mechanical exposure is abstract and probabilistic.

This application translates technical risk indicators directly into executive economics by contrasting:
- **Option A (Intervene Now):** Planned micro-stoppage with minimal downtime, standard labor, and wear part costs.
- **Option B (Run to Failure):** Catastrophic downtime, compounded capacity losses, idle operator standby costs, emergency technician surcharges, express freight, and tooling scrap.

---

## Key Features

1. **Deterministic Decision Engine:** Pure mathematical models outside the LLM. Zero hallucinated figures.
2. **Balanced 1 ➔ 2 ➔ 4 Diverging Tree Factory Topology:**
   - **Stage 1 (Primary Forming Feeder):** M-101 Hydraulic Press (100 pkts/hr | PKR 180,000/hr line loss rate) — Single point of failure.
   - **Stage 2 (Parallel Milling Split):** M-201 CNC Mill A & M-202 CNC Mill B (50 pkts/hr each | PKR 120,000/hr each) — Parallel split (50% capacity loss).
   - **Stage 3 (Automated Packaging Quad Split):** M-301, M-302, M-303, M-304 (25 pkts/hr each | PKR 45,000/hr each) — Quad split (25% loss per cell).
3. **Strategic Savings Dashboard (July – September 2026 MTD):**
   - Cumulative net losses avoided, rescued production hours, approved stops, and enforced safety lockouts.
   - Interactive Plotly monthly cost-vs-loss breakdown.
4. **Hard Statutory Safety Gatekeeper:**
   - Enforces immediate lockout for safety-critical interlocks (OSHA 1910.212 / IEC 62061 SIL-2/3), prohibiting Option B deferral.
5. **Real-time Shift Handover Ledger:**
   - Immutable audit logging of all operator decisions and justifications, downloadable as CSV.

---

## Quickstart

### Prerequisites
- Python 3.10+
- `pip install -r requirements.txt`

### Launch Locally
```bash
streamlit run app.py
```
Or with Python launcher:
```bash
py -m streamlit run app.py
```

### Deploy to Streamlit Cloud
1. Push this repository to GitHub under your account.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Click **"New app"**, choose this repo, and set Main file path to `app.py`.
4. Click **"Deploy"**.
