"""
NASA CMAPSS → CNC spindle sensor mapping.

CMAPSS (Commercial Modular Aero-Propulsion System Simulation) is run-to-failure
turbofan data. For this portfolio demo we treat each engine unit as a CNC
spindle cell and remap a subset of sensors into shop-floor vocabulary.

WHY this works for interviews:
  - Same multivariate degradation structure (healthy → wear → failure).
  - Hiring managers in microtech recognize vibration / temp / current faster
    than "sensor_11" — the proxy is honest if you say it out loud.
  - You are NOT claiming turbofan physics equals CNC physics; you are reusing
    a public degradation trajectory as a stand-in until plant data exists.
"""

from __future__ import annotations

# Official-ish CMAPSS column names (FD001 train/test style).
CMAPSS_COLUMNS = [
    "unit_id",
    "cycle",
    "op_setting_1",
    "op_setting_2",
    "op_setting_3",
    *[f"sensor_{i}" for i in range(1, 22)],
]

# Columns that actually vary under FD001 (others are near-constant).
# Source: widely cited CMAPSS feature notes — we keep only informative ones.
CMAPSS_INFORMATIVE = [
    "sensor_2",
    "sensor_3",
    "sensor_4",
    "sensor_7",
    "sensor_11",
    "sensor_12",
    "sensor_13",
    "sensor_15",
    "sensor_17",
    "sensor_20",
    "sensor_21",
]

# CNC proxy mapping used by demo_data + optional raw CMAPSS loader.
# Each CNC feature is a scaled/renamed view of one CMAPSS sensor.
CMAPSS_TO_CNC: dict[str, str] = {
    # Vibration family — high-frequency / pressure-adjacent channels as RMS proxy
    "sensor_11": "vibration_rms",
    "sensor_15": "vibration_peak",
    # Thermal family
    "sensor_2": "temperature_spindle_c",
    "sensor_3": "temperature_coolant_c",
    # Electrical / load family
    "sensor_4": "current_draw_a",
    "sensor_7": "load_pct",
}

CNC_TO_CMAPSS: dict[str, str] = {v: k for k, v in CMAPSS_TO_CNC.items()}

FRAMING_BLURB = """
Framing for manufacturing audiences
-----------------------------------
Dataset: NASA CMAPSS FD001-style run-to-failure trajectories (public).
Proxy story: each "engine unit" = one CNC spindle cell on a shared job shop floor.
Sensor story: we rename and rescale informative CMAPSS channels into vibration,
temperature, and current/load — the triad a Neuchâtel micro-machining lead would
expect on a first health dashboard.

What we claim: multivariate degradation + unsupervised anomaly scoring works as a
maintenance triage signal.
What we do NOT claim: turbofan aerothermal physics, certified RUL for a specific
machine tool, or OPC-UA plant integration beyond a mock tag layer.
"""
