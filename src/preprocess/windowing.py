"""Sliding-window feature extraction for multivariate sensor streams."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import SENSOR_COLUMNS, WINDOW_SIZE, WINDOW_STRIDE


def _window_stats(block: np.ndarray) -> np.ndarray:
    """
    Compact stats per sensor over the window.

    Features per sensor: mean, std, last, slope (linear).
    WHY these four: IF is distance-based; mean/std/last catch level & volatility,
    slope catches accelerating wear, without FFT / spectrograms (over-engineer trap).
    """
    n_sensors = block.shape[1]
    feats: list[float] = []
    x = np.arange(block.shape[0], dtype=float)
    x_mean = x.mean()
    x_var = ((x - x_mean) ** 2).sum()
    for j in range(n_sensors):
        y = block[:, j]
        feats.append(float(y.mean()))
        feats.append(float(y.std(ddof=0)))
        feats.append(float(y[-1]))
        # Simple least-squares slope
        if x_var == 0:
            slope = 0.0
        else:
            slope = float(((x - x_mean) * (y - y.mean())).sum() / x_var)
        feats.append(slope)
    return np.asarray(feats, dtype=float)


def feature_names(cols: list[str] | None = None) -> list[str]:
    cols = cols or SENSOR_COLUMNS
    names: list[str] = []
    for c in cols:
        names.extend([f"{c}__mean", f"{c}__std", f"{c}__last", f"{c}__slope"])
    return names


def build_windows(
    df: pd.DataFrame,
    *,
    group_col: str = "machine_id",
    time_col: str = "cycle",
    cols: list[str] | None = None,
    window_size: int = WINDOW_SIZE,
    stride: int = WINDOW_STRIDE,
) -> tuple[pd.DataFrame, np.ndarray]:
    """
    Return (meta DataFrame, feature matrix X).

    meta columns: machine_id, cycle_end, timestamp_min (if present)
    """
    cols = cols or SENSOR_COLUMNS
    names = feature_names(cols)
    meta_rows: list[dict] = []
    vectors: list[np.ndarray] = []

    for machine_id, g in df.groupby(group_col, sort=False):
        g = g.sort_values(time_col)
        values = g[cols].astype(float).to_numpy()
        cycles = g[time_col].to_numpy()
        ts = g["timestamp_min"].to_numpy() if "timestamp_min" in g.columns else cycles
        n = len(g)
        if n < window_size:
            continue
        for start in range(0, n - window_size + 1, stride):
            end = start + window_size
            block = values[start:end]
            vectors.append(_window_stats(block))
            meta_rows.append(
                {
                    "machine_id": machine_id,
                    "cycle_end": int(cycles[end - 1]),
                    "timestamp_min": float(ts[end - 1]),
                    "window_start_cycle": int(cycles[start]),
                }
            )

    meta = pd.DataFrame(meta_rows)
    X = np.vstack(vectors) if vectors else np.empty((0, len(names)))
    feat_df = pd.DataFrame(X, columns=names)
    return pd.concat([meta.reset_index(drop=True), feat_df], axis=1), X
