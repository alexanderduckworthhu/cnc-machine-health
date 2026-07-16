"""
Shared visual tokens for Plotly charts and Dash inline styles.

Keep in sync with assets/styles.css custom properties. Charts cannot read CSS
at runtime, so this module is the Python-side source of truth for hex values.
"""

from __future__ import annotations

# Mirror of assets/styles.css :root — change both when adjusting the palette.
COLOR_BG_0 = "#0b1016"
COLOR_BG_1 = "#121a22"
COLOR_PANEL = "#18222d"
COLOR_LINE = "#2a3746"
COLOR_TEXT = "#e8eef4"
COLOR_MUTED = "#8b9aab"
COLOR_ACCENT = "#3d8bfd"
COLOR_GREEN = "#3ecf8e"
COLOR_AMBER = "#e6b84d"
COLOR_RED = "#e85d5d"
COLOR_VIBRATION = "#5ec8ff"
COLOR_TEMPERATURE = "#ff9f6b"
COLOR_CURRENT = "#7dd3c0"
COLOR_COOLANT = "#f0c987"
COLOR_LOAD = "#5eb8a8"
COLOR_FALLBACK = "#8b9aab"

ACCENT_FILL_ALPHA = "rgba(61, 139, 253, 0.12)"

STATUS_COLOR = {
    "green": COLOR_GREEN,
    "amber": COLOR_AMBER,
    "red": COLOR_RED,
}

CHART_COLORS = {
    "grid": COLOR_LINE,
    "text": COLOR_TEXT,
    "muted": COLOR_MUTED,
    "accent": COLOR_ACCENT,
    "green": COLOR_GREEN,
    "amber": COLOR_AMBER,
    "red": COLOR_RED,
    "vibration": COLOR_VIBRATION,
    "temperature": COLOR_TEMPERATURE,
    "current": COLOR_CURRENT,
    "coolant": COLOR_COOLANT,
    "load": COLOR_LOAD,
}

# Chart layout (px)
CHART_HEALTH_HEIGHT_PX = 260
CHART_SENSOR_HEIGHT_PX = 560
CHART_HEALTH_Y_MAX = 105
CHART_TRANSITION_MS = 280
