"""Isolation Forest wrapper for window-level anomaly detection."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from sklearn.ensemble import IsolationForest

from src.config import (
    IF_CONTAMINATION,
    IF_MAX_SAMPLES,
    IF_N_ESTIMATORS,
    MODEL_PATH,
    RANDOM_SEED,
)
from src.io_utils import dump_joblib, load_joblib


def make_isolation_forest(
    *,
    n_estimators: int = IF_N_ESTIMATORS,
    contamination: float = IF_CONTAMINATION,
    max_samples: int | float | str = IF_MAX_SAMPLES,
    random_state: int = RANDOM_SEED,
) -> IsolationForest:
    """Construct an IsolationForest with project defaults."""
    return IsolationForest(
        n_estimators=n_estimators,
        contamination=contamination,
        max_samples=max_samples,
        random_state=random_state,
        n_jobs=-1,
    )


def fit_isolation_forest(feature_matrix: np.ndarray) -> IsolationForest:
    """Fit Isolation Forest on a window feature matrix; return the model."""
    model = make_isolation_forest()
    model.fit(feature_matrix)
    return model


def anomaly_scores(model: IsolationForest, feature_matrix: np.ndarray) -> np.ndarray:
    """
    Return decision_function scores (higher = more normal).

    sklearn IsolationForest: decision_function ≈ score_samples - offset_.
    """
    return model.decision_function(feature_matrix)


def save_model(model: IsolationForest, path: Path | None = None) -> Path:
    """Persist a fitted model; return the path written."""
    target = path or MODEL_PATH
    dump_joblib(target, model)
    return target


def load_model(path: Path | None = None) -> IsolationForest:
    """Load a fitted Isolation Forest from disk."""
    return load_joblib(path or MODEL_PATH)
