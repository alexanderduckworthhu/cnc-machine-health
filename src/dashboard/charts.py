"""Plotly chart builders for the CNC health dashboard."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.config import HEALTH_AMBER_MIN, HEALTH_GREEN_MIN
from src.i18n import DEFAULT_LANG, sensor_label, status_label, t
from src.theme import (
    ACCENT_FILL_ALPHA,
    CHART_COLORS,
    CHART_HEALTH_HEIGHT_PX,
    CHART_HEALTH_Y_MAX,
    CHART_SENSOR_HEIGHT_PX,
    CHART_TRANSITION_MS,
    STATUS_COLOR,
)

SENSOR_LINE_COLORS = {
    "vibration_rms": CHART_COLORS["vibration"],
    "vibration_peak": CHART_COLORS["accent"],
    "temperature_spindle_c": CHART_COLORS["temperature"],
    "temperature_coolant_c": CHART_COLORS["coolant"],
    "current_draw_a": CHART_COLORS["current"],
    "load_pct": CHART_COLORS["load"],
}


def _base_layout(
    fig: go.Figure,
    title: str = "",
    *,
    legend_below: bool = False,
) -> go.Figure:
    """Apply shared dark-theme layout; return the figure."""
    if legend_below:
        legend = dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            x=0,
            xanchor="left",
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        )
        margins = dict(l=48, r=24, t=40, b=110)
    else:
        legend = dict(
            orientation="h",
            yanchor="bottom",
            y=1.12,
            x=0,
            xanchor="left",
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11),
        )
        margins = dict(l=48, r=24, t=56, b=36)

    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color=CHART_COLORS["text"]), x=0.01),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="IBM Plex Sans, Segoe UI, sans-serif",
            color=CHART_COLORS["text"],
            size=12,
        ),
        margin=margins,
        legend=legend,
        hovermode="x unified",
        transition_duration=CHART_TRANSITION_MS,
    )
    fig.update_xaxes(
        gridcolor=CHART_COLORS["grid"],
        zeroline=False,
        color=CHART_COLORS["muted"],
    )
    fig.update_yaxes(
        gridcolor=CHART_COLORS["grid"],
        zeroline=False,
        color=CHART_COLORS["muted"],
    )
    return fig


def health_timeline(
    windows: pd.DataFrame,
    machine_id: str,
    lang: str = DEFAULT_LANG,
) -> go.Figure:
    """Build the health-over-cycles chart for one machine."""
    machine_windows = windows[windows["machine_id"] == machine_id].sort_values(
        "cycle_end"
    )
    title = t("chart_health_title", lang)
    axis_cycle = t("chart_axis_cycle", lang)
    axis_health = t("chart_axis_health", lang)
    fig = go.Figure()
    if machine_windows.empty:
        fig.add_annotation(
            text=t("chart_empty_health", lang),
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(color=CHART_COLORS["muted"]),
        )
        return _base_layout(fig, title)

    fig.add_trace(
        go.Scatter(
            x=machine_windows["cycle_end"],
            y=machine_windows["health"],
            mode="lines",
            name=axis_health,
            line=dict(color=CHART_COLORS["accent"], width=2.5, shape="spline"),
            fill="tozeroy",
            fillcolor=ACCENT_FILL_ALPHA,
            hovertemplate=(
                f"{axis_cycle} %{{x}}<br>{axis_health} %{{y:.0f}}<extra></extra>"
            ),
        )
    )
    fig.add_hline(
        y=HEALTH_GREEN_MIN,
        line_dash="dot",
        line_color=STATUS_COLOR["green"],
        annotation_text=status_label("green", lang),
        annotation_position="top left",
    )
    fig.add_hline(
        y=HEALTH_AMBER_MIN,
        line_dash="dot",
        line_color=STATUS_COLOR["amber"],
        annotation_text=status_label("amber", lang),
        annotation_position="bottom left",
    )
    fig.update_yaxes(range=[0, CHART_HEALTH_Y_MAX], title=axis_health)
    fig.update_xaxes(title=axis_cycle)
    fig.update_layout(height=CHART_HEALTH_HEIGHT_PX)
    return _base_layout(fig, title)


def sensor_traces_figure(
    traces: pd.DataFrame,
    machine_id: str,
    lang: str = DEFAULT_LANG,
) -> go.Figure:
    """Build the three-band sensor chart for one machine."""
    machine_traces = traces[traces["machine_id"] == machine_id].sort_values("cycle")
    title = t("chart_sensor_title", lang)
    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.10,
        subplot_titles=(
            t("subplot_vibration", lang),
            t("subplot_temperature", lang),
            t("subplot_current_load", lang),
        ),
    )
    if machine_traces.empty:
        fig.add_annotation(
            text=t("chart_empty_sensors", lang),
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(color=CHART_COLORS["muted"]),
        )
        return _base_layout(fig, title, legend_below=True)

    channel_groups = [
        (1, ["vibration_rms", "vibration_peak"]),
        (2, ["temperature_spindle_c", "temperature_coolant_c"]),
        (3, ["current_draw_a", "load_pct"]),
    ]
    for row, columns in channel_groups:
        for column in columns:
            label = sensor_label(column, lang)
            fig.add_trace(
                go.Scatter(
                    x=machine_traces["cycle"],
                    y=machine_traces[column],
                    name=label,
                    line=dict(
                        color=SENSOR_LINE_COLORS[column],
                        width=1.8,
                        shape="spline",
                    ),
                    hovertemplate="%{y:.2f}<extra>" + label + "</extra>",
                ),
                row=row,
                col=1,
            )
    fig.update_layout(height=CHART_SENSOR_HEIGHT_PX)
    fig.update_xaxes(title_text=t("chart_axis_cycle", lang), row=3, col=1)
    return _base_layout(fig, title, legend_below=True)
