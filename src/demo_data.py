"""
Synthetic CMAPSS-style CNC sensor traces for offline demos.

Generates run-to-failure trajectories that mimic FD001 structure without
requiring a NASA download. Optional loader accepts real CMAPSS text files
if dropped into data/raw/.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.cmapss_mapping import CMAPSS_TO_CNC
from src.config import (
    CYCLE_MINUTES,
    MACHINE_IDS,
    RANDOM_SEED,
    SAMPLE_DIR,
    SENSOR_COLUMNS,
)


# Baseline operating points in CNC units (healthy regime).
_BASELINES = {
    "vibration_rms": 2.4,
    "vibration_peak": 6.5,
    "temperature_spindle_c": 48.0,
    "temperature_coolant_c": 28.0,
    "current_draw_a": 18.0,
    "load_pct": 55.0,
}

# How strongly each sensor drifts toward failure (multiplicative end-of-life bump).
_EOL_FACTORS = {
    "vibration_rms": 3.2,
    "vibration_peak": 3.8,
    "temperature_spindle_c": 1.55,
    "temperature_coolant_c": 1.35,
    "current_draw_a": 1.7,
    "load_pct": 1.45,
}


def _degradation_curve(n_cycles: int, steepness: float = 3.5) -> np.ndarray:
    """Flat early life, accelerating late wear, better green/amber/red staging."""
    t = np.linspace(0.0, 1.0, n_cycles)
    return t**steepness


def generate_unit_trace(
    machine_id: str,
    n_cycles: int,
    rng: np.random.Generator,
    *,
    miss_rate: float = 0.02,
    fail_early: bool = False,
) -> pd.DataFrame:
    """One machine = one CMAPSS-style unit with CNC-named sensors."""
    deg = _degradation_curve(n_cycles, steepness=4.0 if fail_early else 3.5)
    if fail_early:
        deg = np.clip(deg * 1.15, 0.0, 1.0)

    rows: dict[str, np.ndarray] = {
        "machine_id": np.full(n_cycles, machine_id),
        "cycle": np.arange(1, n_cycles + 1),
        "timestamp_min": np.arange(n_cycles) * CYCLE_MINUTES,
    }

    for col in SENSOR_COLUMNS:
        base = _BASELINES[col]
        eol = base * _EOL_FACTORS[col]
        noise = rng.normal(0.0, 0.03 * base, size=n_cycles)
        # Mild operating-mode oscillation (fixture change / tool path).
        mode = 0.04 * base * np.sin(np.linspace(0, 8 * np.pi, n_cycles) + rng.random())
        signal = base + (eol - base) * deg + noise + mode
        # Inject missingness (sensor dropouts).
        mask = rng.random(n_cycles) < miss_rate
        signal = signal.astype(float)
        signal[mask] = np.nan
        rows[col] = signal

    # Remaining useful life label (cycles), used only for TTF sanity checks / docs.
    rows["rul_cycles"] = np.arange(n_cycles, 0, -1)
    # Provenance tag so demos stay honest in the UI.
    rows["source"] = np.full(n_cycles, "cmapss_proxy_synthetic")
    return pd.DataFrame(rows)


def build_demo_fleet(
    machine_ids: list[str] | None = None,
    seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    """
    Four machines with distinct health stories for the dashboard cards.

    Each unit is generated as a full run-to-failure curve, then truncated to a
    life fraction so "now" is mid-life (green), watch (amber), or near EOL (red).
    """
    rng = np.random.default_rng(seed)
    machine_ids = machine_ids or list(MACHINE_IDS)

    # full_n = underlying degradation length; keep_frac = where "now" sits on that curve
    profiles = {
        machine_ids[0]: {"full_n": 280, "keep_frac": 0.35, "fail_early": False},  # green
        machine_ids[1]: {"full_n": 260, "keep_frac": 0.78, "fail_early": True},  # amber
        machine_ids[2]: {"full_n": 240, "keep_frac": 0.95, "fail_early": True},  # red
        machine_ids[3]: {"full_n": 270, "keep_frac": 0.48, "fail_early": False},  # green
    }
    frames = []
    for mid in machine_ids:
        p = profiles[mid]
        full = generate_unit_trace(
            mid,
            p["full_n"],
            rng,
            fail_early=p["fail_early"],
        )
        keep = max(int(p["full_n"] * p["keep_frac"]), 40)
        frames.append(full.iloc[:keep].copy())
    return pd.concat(frames, ignore_index=True)


def save_demo_sample(out_dir: Path | None = None) -> Path:
    out_dir = out_dir or SAMPLE_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "sensor_traces.csv"
    df = build_demo_fleet()
    df.to_csv(path, index=False)
    return path


def load_cmapss_txt(path: Path) -> pd.DataFrame:
    """
    Optional: load a real NASA CMAPSS train_FD00x.txt and rename to CNC columns.

    File format: space-separated, no header, 26 columns (unit, cycle, 3 ops, 21 sensors).
    """
    from src.cmapss_mapping import CMAPSS_COLUMNS

    raw = pd.read_csv(path, sep=r"\s+", header=None, names=CMAPSS_COLUMNS)
    keep = ["unit_id", "cycle", *CMAPSS_TO_CNC.keys()]
    slim = raw[keep].copy()
    slim = slim.rename(columns={"unit_id": "machine_id", **CMAPSS_TO_CNC})
    slim["machine_id"] = slim["machine_id"].map(lambda u: f"CNC-{int(u):02d}")
    slim["timestamp_min"] = (slim["cycle"] - 1) * CYCLE_MINUTES
    # Min-max rescale each mapped sensor into plausible CNC ranges (demo only).
    from src.config import PLAUSIBLE_RANGES

    for col in SENSOR_COLUMNS:
        if col not in slim.columns:
            continue
        lo, hi = PLAUSIBLE_RANGES[col]
        # Stay inside 20–80% of the plausible band so IF sees room to degrade.
        target_lo = lo + 0.2 * (hi - lo)
        target_hi = lo + 0.8 * (hi - lo)
        s = slim[col].astype(float)
        s_min, s_max = s.min(), s.max()
        if s_max > s_min:
            slim[col] = target_lo + (s - s_min) / (s_max - s_min) * (target_hi - target_lo)
        slim["source"] = "cmapss_fd_raw"
    return slim


def load_sensor_traces(path: Path | None = None) -> pd.DataFrame:
    path = path or (SAMPLE_DIR / "sensor_traces.csv")
    return pd.read_csv(path)
