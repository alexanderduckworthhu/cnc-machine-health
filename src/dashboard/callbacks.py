"""Dash callbacks — cell selection and language drive the whole view."""

from __future__ import annotations

import json
from typing import Any

import pandas as pd
from dash import ALL, Dash, Input, Output, State, callback_context, html, no_update

from src.copy import (
    detail_health_line,
    floor_summary,
    opcua_banner,
    viewing_pill,
)
from src.dashboard.charts import health_timeline, sensor_traces_figure
from src.dashboard.helpers import status_sort_rank
from src.dashboard.layout import alert_items, machine_card
from src.i18n import (
    DEFAULT_LANG,
    machine_label,
    normalize_lang,
    sensor_label,
    status_hint,
    t,
)
from src.pipeline import load_clean_traces, load_windows
from src.ttf import format_ttf

_TRACES_CACHE: pd.DataFrame | None = None
_WINDOWS_CACHE: pd.DataFrame | None = None


def _cached_traces() -> pd.DataFrame:
    """Return cleaned sensor traces, loading from disk once per process."""
    global _TRACES_CACHE
    if _TRACES_CACHE is None:
        _TRACES_CACHE = load_clean_traces()
    return _TRACES_CACHE


def _cached_windows() -> pd.DataFrame:
    """Return scored windows, loading from disk once per process."""
    global _WINDOWS_CACHE
    if _WINDOWS_CACHE is None:
        _WINDOWS_CACHE = load_windows()
    return _WINDOWS_CACHE


def register_callbacks(app: Dash) -> None:
    """Attach selection, language, and view-refresh callbacks."""

    @app.callback(
        Output("selected-machine", "data"),
        Input({"type": "machine-card", "index": ALL}, "n_clicks"),
        State("selected-machine", "data"),
        prevent_initial_call=True,
    )
    def pick_machine(
        _card_clicks: list[int | None],
        current_machine: str,
    ) -> str:
        """Update the selected machine when a health card is clicked."""
        ctx = callback_context
        if not ctx.triggered:
            return no_update
        trigger_id = ctx.triggered[0]["prop_id"]
        if "machine-card" not in trigger_id:
            return no_update
        payload = json.loads(trigger_id.rsplit(".", 1)[0])
        return str(payload["index"])

    @app.callback(
        Output("brand-eyebrow", "children"),
        Output("brand-title", "children"),
        Output("brand-tagline", "children"),
        Output("lang-label", "children"),
        Output("floor-summary", "children"),
        Output("floor-hint", "children"),
        Output("panel-main-title", "children"),
        Output("panel-side-title", "children"),
        Output("panel-notes-title", "children"),
        Output("app-footer", "children"),
        Output("opcua-banner", "children"),
        Output("card-row", "children"),
        Output("card-row", "aria-label"),
        Output("viewing-pill", "children"),
        Output("alert-feed", "children"),
        Output("selection-detail", "children"),
        Output("sensor-graph", "figure"),
        Output("health-graph", "figure"),
        Output("health-graph-wrap", "aria-label"),
        Output("sensor-graph-wrap", "aria-label"),
        Input("selected-machine", "data"),
        Input("language-select", "value"),
        State("snapshots-store", "data"),
        State("alerts-store", "data"),
        State("opcua-node-count", "data"),
    )
    def refresh_view(
        machine_id: str,
        language: str | None,
        snapshots: list[dict[str, Any]] | None,
        alerts: list[dict[str, Any]] | None,
        node_count: int | None,
    ) -> tuple[Any, ...]:
        """Rebuild chrome, cards, notes, and charts for selection + language."""
        lang = normalize_lang(language or DEFAULT_LANG)
        snapshots = snapshots or []
        alerts = alerts or []
        ordered = sorted(
            snapshots,
            key=lambda snap: (
                status_sort_rank(snap.get("status", "")),
                snap["machine_id"],
            ),
        )
        cards = [
            machine_card(snap, selected=(snap["machine_id"] == machine_id), lang=lang)
            for snap in ordered
        ]
        snapshot = next(
            (snap for snap in snapshots if snap["machine_id"] == machine_id),
            {},
        )
        status = snapshot.get("status", "green")
        health_value = float(snapshot.get("health", 0.0))
        ttf_display = format_ttf(health_value, lang)

        detail = html.Div(
            [
                html.P(
                    [
                        html.Strong(machine_id),
                        html.Span(f" — {machine_label(machine_id, lang)}"),
                    ],
                    className="detail-title",
                ),
                html.P(
                    detail_health_line(health_value, status, ttf_display, lang),
                    className="detail-health",
                ),
                html.P(status_hint(status, lang), className="detail-hint"),
                html.Details(
                    [
                        html.Summary(t("sensor_details", lang)),
                        html.Ul(
                            [
                                html.Li(
                                    f"{sensor_label(key, lang)}: {value}"
                                )
                                for key, value in (
                                    snapshot.get("latest_sensors") or {}
                                ).items()
                            ],
                            className="sensor-list",
                        ),
                    ],
                    className="sensor-details",
                ),
            ],
            className="selection-body",
        )

        traces = _cached_traces()
        windows = _cached_windows()
        n_nodes = node_count if isinstance(node_count, int) else 32

        return (
            t("brand_eyebrow", lang),
            t("app_title", lang),
            t("tagline", lang),
            t("lang", lang),
            floor_summary(snapshots, lang),
            t("floor_hint", lang),
            t("panel_main", lang),
            t("panel_side", lang),
            t("panel_notes", lang),
            t("disclaimer", lang),
            opcua_banner(n_nodes, lang),
            cards,
            t("cards_aria", lang),
            viewing_pill(machine_id, lang),
            alert_items(alerts, machine_id, lang),
            detail,
            sensor_traces_figure(traces, machine_id, lang),
            health_timeline(windows, machine_id, lang),
            t("health_graph_aria", lang),
            t("sensor_graph_aria", lang),
        )
