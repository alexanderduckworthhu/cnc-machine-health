"""
Locked modeling / framing choices for the CNC health portfolio project.

WHY comments are intentional — they are interview talking points in code form.
Change a knob only if you can rewrite the WHY sentence.
"""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
SAMPLE_DIR = DATA_DIR / "sample"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
MODEL_DIR = DATA_DIR / "models"
ASSETS_DIR = PROJECT_ROOT / "assets"

# --- Demo fleet --------------------------------------------------------------
# WHY 4 machines: enough for a floor-board story without a fake 40-asset SCADA wall.
MACHINE_IDS = ["CNC-01", "CNC-02", "CNC-03", "CNC-04"]
MACHINE_LABELS = {
    "CNC-01": "Spindle cell A — bridge mill",
    "CNC-02": "Spindle cell B — turning center",
    "CNC-03": "Micro-milling — watch plate fixture",
    "CNC-04": "Deburr / finish — shared cell",
}

# --- Sensors -----------------------------------------------------------------
# WHY these three families: vibration / temperature / current are the minimum
# credible triad for spindle health on a Swiss microtech floor.
SENSOR_COLUMNS = [
    "vibration_rms",
    "vibration_peak",
    "temperature_spindle_c",
    "temperature_coolant_c",
    "current_draw_a",
    "load_pct",
]

SENSOR_DISPLAY = {
    "vibration_rms": "Vibration RMS (mm/s)",
    "vibration_peak": "Vibration peak (mm/s)",
    "temperature_spindle_c": "Spindle temp (°C)",
    "temperature_coolant_c": "Coolant temp (°C)",
    "current_draw_a": "Spindle current (A)",
    "load_pct": "Axis load (%)",
}

PLAUSIBLE_RANGES: dict[str, tuple[float, float]] = {
    "vibration_rms": (0.0, 25.0),
    "vibration_peak": (0.0, 60.0),
    "temperature_spindle_c": (15.0, 120.0),
    "temperature_coolant_c": (5.0, 80.0),
    "current_draw_a": (0.0, 80.0),
    "load_pct": (0.0, 120.0),
}

# --- Time-series windowing ---------------------------------------------------
WINDOW_SIZE = 30
WINDOW_STRIDE = 3
FORWARD_FILL_LIMIT_CYCLES = 3

# --- Isolation Forest --------------------------------------------------------
IF_N_ESTIMATORS = 200
IF_CONTAMINATION = 0.05
IF_MAX_SAMPLES = "auto"
IF_HEALTHY_FRACTION = 0.50
MIN_HEALTHY_TRAIN_WINDOWS = 20
RANDOM_SEED = 42

# --- Health score (0–100) ----------------------------------------------------
HEALTH_GREEN_MIN = 75.0
HEALTH_AMBER_MIN = 50.0
HEALTH_DROP_ALERT_POINTS = 15.0
HEALTH_AT_MEDIAN = 85.0
HEALTH_PER_Z_UNIT = 12.0
MAD_TO_SIGMA = 1.4826
NUMERIC_EPS = 1e-9

# --- Time-to-failure proxy ---------------------------------------------------
TTF_HEALTH_REF = 50.0
TTF_AT_REF_CYCLES = 40.0
TTF_MAX_CYCLES = 200.0
CYCLE_MINUTES = 6.0
TTF_DAYS_THRESHOLD_HOURS = 48.0

# --- UI limits ---------------------------------------------------------------
ALERT_FEED_LIMIT = 8
DASH_HOST = "0.0.0.0"
DASH_PORT = 8050

# --- OPC-UA mock -------------------------------------------------------------
OPCUA_ENDPOINT = "opc.tcp://127.0.0.1:4840/cnc-health/"
OPCUA_NAMESPACE = 2

# --- Paths -------------------------------------------------------------------
MODEL_PATH = MODEL_DIR / "isolation_forest.joblib"
SCALER_PATH = MODEL_DIR / "window_scaler.joblib"
SCORE_CALIB_PATH = MODEL_DIR / "score_calibration.joblib"
SENSOR_TRACE_PATH = SAMPLE_DIR / "sensor_traces.csv"
WINDOWS_CSV_PATH = PROCESSED_DIR / "windows.csv"
CLEAN_TRACES_PATH = PROCESSED_DIR / "sensor_traces_clean.csv"
SNAPSHOTS_PATH = PROCESSED_DIR / "machine_snapshots.json"
ALERTS_PATH = PROCESSED_DIR / "alerts.json"
METADATA_PATH = PROCESSED_DIR / "metadata.json"

# Legacy alias used by preprocess.missing
FORWARD_FILL_LIMIT = FORWARD_FILL_LIMIT_CYCLES
