"""End-to-end pipeline: clean → window → Isolation Forest → health → alerts."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.config import (
    ALERTS_PATH,
    CLEAN_TRACES_PATH,
    HEALTH_AMBER_MIN,
    HEALTH_DROP_ALERT_POINTS,
    HEALTH_GREEN_MIN,
    IF_HEALTHY_FRACTION,
    MACHINE_IDS,
    MACHINE_LABELS,
    METADATA_PATH,
    MIN_HEALTHY_TRAIN_WINDOWS,
    MODEL_PATH,
    PROCESSED_DIR,
    SAMPLE_DIR,
    SCALER_PATH,
    SCORE_CALIB_PATH,
    SENSOR_COLUMNS,
    SENSOR_TRACE_PATH,
    SNAPSHOTS_PATH,
    WINDOWS_CSV_PATH,
)
from src.copy import alert_message, drop_alert_message
from src.demo_data import load_sensor_traces, save_demo_sample
from src.io_utils import ArtefactLoadError, dump_joblib, read_csv, read_json, write_csv, write_json
from src.models.health_score import (
    fit_calibration,
    save_calibration,
    status_from_health,
    status_label,
)
from src.models.isolation_forest import anomaly_scores, fit_isolation_forest, save_model
from src.preprocess.missing import clean_sensor_frame
from src.preprocess.normalize import fit_scaler, transform_sensors
from src.preprocess.windowing import build_windows, feature_names
from src.ttf import format_ttf, ttf_cycles_from_health, ttf_hours_from_health

STATUS_SORT_RANK = {"red": 0, "amber": 1, "green": 2}
SEVERITY_SORT_RANK = {"high": 0, "medium": 1, "low": 2}


def ensure_sample_data() -> Path:
    """Create the demo sensor CSV if missing; return its path."""
    if not SENSOR_TRACE_PATH.exists():
        return save_demo_sample(SAMPLE_DIR)
    return SENSOR_TRACE_PATH


def _healthy_regime_mask(windows: pd.DataFrame) -> np.ndarray:
    """Return a boolean mask for early-life (healthy-regime) training windows."""
    mask = np.zeros(len(windows), dtype=bool)
    for _, machine_windows in windows.groupby("machine_id"):
        cutoff_cycle = float(machine_windows["cycle_end"].max()) * IF_HEALTHY_FRACTION
        index = machine_windows.index.to_numpy()
        mask[index] = machine_windows["cycle_end"].to_numpy() <= cutoff_cycle
    if int(mask.sum()) < MIN_HEALTHY_TRAIN_WINDOWS:
        fallback_n = max(len(windows) // 2, MIN_HEALTHY_TRAIN_WINDOWS)
        mask = np.arange(len(windows)) < fallback_n
    return mask


def run_pipeline(
    traces: pd.DataFrame | None = None,
    *,
    persist: bool = True,
) -> dict[str, Any]:
    """
    Train Isolation Forest on healthy-regime windows and emit fleet snapshots.

    Returns a dict with traces_clean, windows, snapshots, alerts, meta, model,
    scaler, and calibration.
    """
    ensure_sample_data()
    raw_traces = traces if traces is not None else load_sensor_traces()
    clean_traces = clean_sensor_frame(raw_traces)

    scaler = fit_scaler(clean_traces)
    scaled_traces = transform_sensors(clean_traces, scaler)
    windows, feature_matrix = build_windows(scaled_traces)
    if len(feature_matrix) == 0:
        raise RuntimeError(
            "No windows built — check WINDOW_SIZE against trace length per machine."
        )

    healthy_mask = _healthy_regime_mask(windows)
    train_matrix = feature_matrix[healthy_mask]
    model = fit_isolation_forest(train_matrix)
    calibration = fit_calibration(anomaly_scores(model, train_matrix))
    if_scores = anomaly_scores(model, feature_matrix)
    health_scores = calibration.health(if_scores)

    scored_windows = windows.copy()
    scored_windows["if_score"] = if_scores
    scored_windows["health"] = health_scores
    scored_windows["status"] = [status_from_health(float(h)) for h in health_scores]
    scored_windows["ttf_cycles"] = [ttf_cycles_from_health(float(h)) for h in health_scores]
    scored_windows["ttf_hours"] = [ttf_hours_from_health(float(h)) for h in health_scores]

    snapshots: list[dict[str, Any]] = []
    alerts: list[dict[str, Any]] = []

    for machine_id in MACHINE_IDS:
        machine_windows = scored_windows[scored_windows["machine_id"] == machine_id]
        if machine_windows.empty:
            continue
        latest = machine_windows.iloc[-1]
        health = float(latest["health"])
        status = status_from_health(health)
        machine_sensors = clean_traces.loc[clean_traces["machine_id"] == machine_id]
        snapshots.append(
            {
                "machine_id": machine_id,
                "label": MACHINE_LABELS.get(machine_id, machine_id),
                "health": round(health, 1),
                "status": status,
                "status_label": status_label(status),
                "ttf_cycles": round(float(latest["ttf_cycles"]), 1),
                "ttf_hours": round(float(latest["ttf_hours"]), 2),
                "ttf_display": format_ttf(health),
                "cycle_end": int(latest["cycle_end"]),
                "if_score": round(float(latest["if_score"]), 4),
                "latest_sensors": {
                    column: round(float(machine_sensors[column].iloc[-1]), 3)
                    for column in SENSOR_COLUMNS
                },
            }
        )

        if status in ("amber", "red"):
            alerts.append(
                {
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "machine_id": machine_id,
                    "severity": "high" if status == "red" else "medium",
                    "status": status,
                    "kind": "status",
                    "health": round(health, 1),
                    "ttf_display": format_ttf(health),
                    "message": alert_message(
                        machine_id, health, status, format_ttf(health)
                    ),
                }
            )
        if len(machine_windows) >= 2:
            previous_health = float(machine_windows.iloc[-2]["health"])
            if previous_health - health >= HEALTH_DROP_ALERT_POINTS:
                alerts.append(
                    {
                        "ts": datetime.now(timezone.utc).isoformat(),
                        "machine_id": machine_id,
                        "severity": "medium",
                        "status": status,
                        "kind": "drop",
                        "health": round(health, 1),
                        "previous_health": round(previous_health, 1),
                        "ttf_display": format_ttf(health),
                        "message": drop_alert_message(
                            machine_id, previous_health, health
                        ),
                    }
                )

    alerts.sort(
        key=lambda note: (
            SEVERITY_SORT_RANK.get(note["severity"], 9),
            note["machine_id"],
        )
    )
    snapshots.sort(
        key=lambda snap: (
            STATUS_SORT_RANK.get(snap["status"], 9),
            snap["machine_id"],
        )
    )

    metadata = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "n_rows": int(len(clean_traces)),
        "n_windows": int(len(scored_windows)),
        "n_train_windows": int(healthy_mask.sum()),
        "n_machines": int(scored_windows["machine_id"].nunique()),
        "feature_names": feature_names(),
        "source": (
            str(clean_traces["source"].iloc[0])
            if "source" in clean_traces.columns
            else "unknown"
        ),
        "model": "IsolationForest",
        "train_regime": f"early {IF_HEALTHY_FRACTION:.0%} of each machine's cycles",
        "health_formula": (
            "clip(85 + 12 * robust_z(IF.decision_function | healthy regime), 0, 100)"
        ),
        "thresholds": {
            "green_min": HEALTH_GREEN_MIN,
            "amber_min": HEALTH_AMBER_MIN,
        },
    }

    if persist:
        try:
            PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
            MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
            save_model(model, MODEL_PATH)
            dump_joblib(SCALER_PATH, scaler)
            save_calibration(calibration, SCORE_CALIB_PATH)
            write_json(SNAPSHOTS_PATH, snapshots)
            write_json(ALERTS_PATH, alerts)
            write_json(METADATA_PATH, metadata)
            write_csv(WINDOWS_CSV_PATH, scored_windows)
            write_csv(CLEAN_TRACES_PATH, clean_traces)
        except ArtefactLoadError:
            raise

    return {
        "traces_clean": clean_traces,
        "windows": scored_windows,
        "snapshots": snapshots,
        "alerts": alerts,
        "meta": metadata,
        "model": model,
        "scaler": scaler,
        "calibration": calibration,
    }


def _ensure_pipeline_artefacts() -> None:
    """Run the pipeline when required processed artefacts are missing."""
    if not SNAPSHOTS_PATH.exists() or not WINDOWS_CSV_PATH.exists():
        run_pipeline(persist=True)


def load_snapshots() -> list[dict[str, Any]]:
    """Load per-machine health snapshots; rebuild artefacts if missing."""
    _ensure_pipeline_artefacts()
    payload = read_json(SNAPSHOTS_PATH)
    if not isinstance(payload, list):
        raise ArtefactLoadError(f"Expected a list in {SNAPSHOTS_PATH}")
    return payload


def load_alerts() -> list[dict[str, Any]]:
    """Load maintenance alerts; rebuild artefacts if missing."""
    _ensure_pipeline_artefacts()
    payload = read_json(ALERTS_PATH)
    if not isinstance(payload, list):
        raise ArtefactLoadError(f"Expected a list in {ALERTS_PATH}")
    return payload


def load_windows() -> pd.DataFrame:
    """Load scored window features used by the health timeline chart."""
    _ensure_pipeline_artefacts()
    return read_csv(WINDOWS_CSV_PATH)


def load_clean_traces() -> pd.DataFrame:
    """Load cleaned sensor traces used by the sensor chart and OPC-UA mock."""
    _ensure_pipeline_artefacts()
    return read_csv(CLEAN_TRACES_PATH)
