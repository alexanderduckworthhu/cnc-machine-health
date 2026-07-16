"""
Health score (0–100) from Isolation Forest anomaly scores.

  z = (score - median_healthy) / (MAD_TO_SIGMA * mad)
  health = clip(HEALTH_AT_MEDIAN + HEALTH_PER_Z_UNIT * z, 0, 100)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from src.config import (
    HEALTH_AMBER_MIN,
    HEALTH_AT_MEDIAN,
    HEALTH_GREEN_MIN,
    HEALTH_PER_Z_UNIT,
    MAD_TO_SIGMA,
    NUMERIC_EPS,
    SCORE_CALIB_PATH,
)
from src.copy import STATUS_LABEL
from src.io_utils import dump_joblib, load_joblib


@dataclass
class ScoreCalibration:
    """Robust location/scale of healthy-regime Isolation Forest scores."""

    median: float
    mad: float

    def health(self, scores: np.ndarray) -> np.ndarray:
        """Map decision_function scores to health in [0, 100]."""
        score_array = np.asarray(scores, dtype=float)
        scale = MAD_TO_SIGMA * max(self.mad, NUMERIC_EPS)
        z_scores = (score_array - self.median) / scale
        return np.clip(HEALTH_AT_MEDIAN + HEALTH_PER_Z_UNIT * z_scores, 0.0, 100.0)


def fit_calibration(train_scores: np.ndarray) -> ScoreCalibration:
    """Fit median/MAD calibration on healthy-regime IF scores."""
    scores = np.asarray(train_scores, dtype=float)
    median = float(np.median(scores))
    mad = float(np.median(np.abs(scores - median)))
    if mad < NUMERIC_EPS:
        mad = float(np.std(scores) + NUMERIC_EPS)
    return ScoreCalibration(median=median, mad=mad)


def status_from_health(health: float) -> str:
    """Return green / amber / red from a health score."""
    if health >= HEALTH_GREEN_MIN:
        return "green"
    if health >= HEALTH_AMBER_MIN:
        return "amber"
    return "red"


def status_label(status: str) -> str:
    """Return shop-floor label for a status key."""
    return STATUS_LABEL.get(status, status)


def save_calibration(calibration: ScoreCalibration, path: Path | None = None) -> Path:
    """Persist calibration to disk; return the path written."""
    target = path or SCORE_CALIB_PATH
    dump_joblib(target, calibration)
    return target


def load_calibration(path: Path | None = None) -> ScoreCalibration:
    """Load calibration from disk."""
    return load_joblib(path or SCORE_CALIB_PATH)
