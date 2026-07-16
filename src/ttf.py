"""
Time-to-failure proxy from health score.

  ttf_cycles = TTF_MAX_CYCLES * (health / 100) ** gamma

gamma is chosen so health=TTF_HEALTH_REF ≈ TTF_AT_REF_CYCLES.
"""

from __future__ import annotations

import math

import numpy as np

from src.config import (
    CYCLE_MINUTES,
    TTF_AT_REF_CYCLES,
    TTF_DAYS_THRESHOLD_HOURS,
    TTF_HEALTH_REF,
    TTF_MAX_CYCLES,
)


def _gamma() -> float:
    """Return the power-curve exponent linking health to remaining cycles."""
    return math.log(TTF_AT_REF_CYCLES / TTF_MAX_CYCLES) / math.log(
        TTF_HEALTH_REF / 100.0
    )


def ttf_cycles_from_health(health: float | np.ndarray) -> float | np.ndarray:
    """Map health score(s) to estimated remaining cycles."""
    health_array = np.clip(np.asarray(health, dtype=float), 1.0, 100.0)
    cycles = TTF_MAX_CYCLES * (health_array / 100.0) ** _gamma()
    cycles = np.clip(cycles, 0.0, TTF_MAX_CYCLES)
    if np.isscalar(health):
        return float(cycles)
    return cycles


def ttf_hours_from_health(health: float | np.ndarray) -> float | np.ndarray:
    """Map health score(s) to estimated remaining hours of cutting."""
    cycles = ttf_cycles_from_health(health)
    hours = np.asarray(cycles) * CYCLE_MINUTES / 60.0
    if np.isscalar(health):
        return float(hours)
    return hours


def format_ttf(health: float, lang: str = "en") -> str:
    """Return a short human remaining-time string for a health score."""
    from src.i18n import t

    hours = float(ttf_hours_from_health(health))
    if hours >= TTF_DAYS_THRESHOLD_HOURS:
        return t("ttf_days", lang, n=hours / 24.0)
    if hours >= 1.0:
        return t("ttf_hours", lang, n=hours)
    return t("ttf_minutes", lang, n=hours * 60.0)
