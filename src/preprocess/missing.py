"""Missing-value handling for multivariate CNC sensor streams."""

from __future__ import annotations

import pandas as pd

from src.config import FORWARD_FILL_LIMIT, PLAUSIBLE_RANGES, SENSOR_COLUMNS


def apply_plausibility_bounds(
    df: pd.DataFrame,
    ranges: dict[str, tuple[float, float]] | None = None,
    cols: list[str] | None = None,
) -> pd.DataFrame:
    """Out-of-range values → NaN. Do not clip, clipping invents machine physics."""
    ranges = ranges or PLAUSIBLE_RANGES
    cols = cols or SENSOR_COLUMNS
    out = df.copy()
    for col in cols:
        if col not in out.columns:
            continue
        lo, hi = ranges[col]
        bad = (out[col] < lo) | (out[col] > hi)
        out.loc[bad, col] = pd.NA
    return out


def forward_fill_limited(
    df: pd.DataFrame,
    group_col: str = "machine_id",
    cols: list[str] | None = None,
    limit: int = FORWARD_FILL_LIMIT,
) -> pd.DataFrame:
    """
    Short dropouts get ffill; longer gaps stay missing.

    WHY: a 1–3 cycle gap is a glitch; a 20-cycle gap is a different story and
    should surface as a missingness flag, not a silently invented trend.
    """
    cols = cols or SENSOR_COLUMNS
    out = df.copy()
    for col in cols:
        if col not in out.columns:
            continue
        out[col] = out.groupby(group_col, sort=False)[col].ffill(limit=limit)
    return out


def add_missingness_flags(
    df: pd.DataFrame,
    cols: list[str] | None = None,
) -> pd.DataFrame:
    cols = cols or SENSOR_COLUMNS
    out = df.copy()
    for col in cols:
        if col not in out.columns:
            continue
        out[f"{col}_was_missing"] = out[col].isna().astype(int)
    return out


def impute_remaining_with_group_median(
    df: pd.DataFrame,
    group_col: str = "machine_id",
    cols: list[str] | None = None,
) -> pd.DataFrame:
    """Last resort for leading NaNs after ffill, use per-machine median."""
    cols = cols or SENSOR_COLUMNS
    out = df.copy()
    for col in cols:
        if col not in out.columns:
            continue
        med = out.groupby(group_col)[col].transform("median")
        out[col] = out[col].fillna(med)
        # Global median if an entire machine column is empty (pathological).
        out[col] = out[col].fillna(out[col].median())
    return out


def clean_sensor_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Full missingness pipeline: bounds → flags → ffill → median."""
    out = apply_plausibility_bounds(df)
    out = add_missingness_flags(out)
    out = forward_fill_limited(out)
    out = impute_remaining_with_group_median(out)
    return out
