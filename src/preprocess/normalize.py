"""Global StandardScaler for sensor columns (shared fleet feature space)."""

from __future__ import annotations

import pandas as pd
from sklearn.preprocessing import StandardScaler

from src.config import SENSOR_COLUMNS


def fit_scaler(
    sensor_frame: pd.DataFrame,
    cols: list[str] | None = None,
) -> StandardScaler:
    """
    Fit a global StandardScaler on cleaned sensor rows; return the scaler.

    WHY global (not per-machine): Isolation Forest needs a shared feature space
    across the fleet; per-machine z-scores hide cross-cell comparisons.
    """
    columns = cols or SENSOR_COLUMNS
    scaler = StandardScaler()
    scaler.fit(sensor_frame[columns].astype(float).to_numpy())
    return scaler


def transform_sensors(
    sensor_frame: pd.DataFrame,
    scaler: StandardScaler,
    cols: list[str] | None = None,
) -> pd.DataFrame:
    """Apply a fitted StandardScaler to sensor columns; return a new frame."""
    columns = cols or SENSOR_COLUMNS
    scaled = sensor_frame.copy()
    scaled[columns] = scaler.transform(scaled[columns].astype(float).to_numpy())
    return scaled
