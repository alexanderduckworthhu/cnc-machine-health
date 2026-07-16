"""Dash layout: one-click cell cards → traces + notes for that cell."""

from __future__ import annotations

from typing import Any

from dash import dcc, html

from src.config import ALERT_FEED_LIMIT
from src.copy import (
    alert_message,
    detail_health_line,
    drop_alert_message,
    empty_alerts_for_machine,
    empty_alerts_floor,
    floor_summary,
    machine_card_aria,
)
from src.dashboard.helpers import status_sort_rank
from src.i18n import (
    DEFAULT_LANG,
    language_dropdown_options,
    machine_label,
    severity_label,
    status_label,
    t,
)
from src.theme import COLOR_ACCENT, STATUS_COLOR
from src.ttf import format_ttf


def _status_dot(status: str) -> html.Span:
    """Return a colored status marker with a text-equivalent nearby via badge."""
    return html.Span(
        className=f"status-dot status-dot-{status}",
        style={"backgroundColor": STATUS_COLOR.get(status, COLOR_ACCENT)},
        **{"aria-hidden": "true"},
    )


def machine_card(
    snapshot: dict[str, Any],
    selected: bool = False,
    lang: str = DEFAULT_LANG,
) -> html.Button:
    """Return a clickable machine health card button."""
    status = snapshot["status"]
    label = status_label(status, lang)
    health = float(snapshot["health"])
    ttf = format_ttf(health, lang)
    classes = f"machine-card status-{status}"
    if selected:
        classes += " is-selected"
    return html.Button(
        [
            html.Div(
                [
                    _status_dot(status),
                    html.Span(snapshot["machine_id"], className="card-id"),
                    html.Span(label, className=f"badge badge-{status}"),
                ],
                className="card-top",
            ),
            html.Div(
                [
                    html.Span(f"{health:.0f}", className="card-health"),
                    html.Span(t("health_denom", lang), className="card-health-denom"),
                ],
                className="card-health-row",
            ),
            html.Div(
                [
                    html.Span(t("roughly_left_prefix", lang), className="muted"),
                    html.Span(ttf, className="card-ttf"),
                    html.Span(t("roughly_left_suffix", lang), className="muted"),
                ],
                className="card-meta",
            ),
            html.Div(machine_label(snapshot["machine_id"], lang), className="card-label"),
            html.Span(
                t("card_cta_selected", lang) if selected else t("card_cta", lang),
                className="card-cta",
            ),
        ],
        id={"type": "machine-card", "index": snapshot["machine_id"]},
        n_clicks=0,
        className=classes,
        title=t("card_tooltip", lang),
        **{
            "aria-label": machine_card_aria(
                snapshot["machine_id"], status, health, lang
            ),
            "aria-pressed": "true" if selected else "false",
        },
    )


def _render_alert_message(note: dict[str, Any], lang: str) -> str:
    """Rebuild an alert message in the active UI language."""
    machine_id = str(note.get("machine_id", ""))
    health = float(note.get("health", 0.0))
    kind = note.get("kind", "status")
    if kind == "drop":
        previous = float(note.get("previous_health", health))
        return drop_alert_message(machine_id, previous, health, lang)
    status = str(note.get("status", "amber"))
    ttf = note.get("ttf_display") or format_ttf(health, lang)
    return alert_message(machine_id, health, status, str(ttf), lang)


def alert_items(
    alerts: list[dict[str, Any]],
    machine_id: str | None = None,
    lang: str = DEFAULT_LANG,
) -> list[html.Li]:
    """Return alert list items scoped to a machine (or the whole floor)."""
    scoped = [
        note
        for note in alerts
        if machine_id is None or note.get("machine_id") == machine_id
    ]
    if not scoped:
        message = (
            empty_alerts_floor(lang)
            if machine_id is None
            else empty_alerts_for_machine(machine_id, lang)
        )
        return [html.Li(message, className="alert-item alert-empty")]

    items: list[html.Li] = []
    for note in scoped[:ALERT_FEED_LIMIT]:
        severity = note.get("severity", "low")
        items.append(
            html.Li(
                [
                    html.Span(
                        severity_label(severity, lang),
                        className=f"sev sev-{severity}",
                    ),
                    html.Span(_render_alert_message(note, lang), className="alert-msg"),
                ],
                className="alert-item",
            )
        )
    return items


def error_layout(message: str, lang: str = DEFAULT_LANG) -> html.Div:
    """Return a full-page recovery layout when artefacts fail to load."""
    return html.Div(
        [
            html.H1(t("bootstrap_error_title", lang), className="brand"),
            html.P(str(message), className="detail-hint"),
            html.P(t("bootstrap_error_hint", lang), className="detail-health"),
            html.Footer(t("disclaimer", lang), className="footer"),
        ],
        className="app-shell error-shell",
        role="alert",
    )


def build_layout(
    snapshots: list[dict[str, Any]],
    alerts: list[dict[str, Any]],
    opcua_banner_text: str,
    default_machine: str | None = None,
    lang: str = DEFAULT_LANG,
    opcua_node_count: int = 32,
) -> html.Div:
    """Return the main dashboard layout tree."""
    if not snapshots:
        return html.Div(
            [
                html.H1(t("app_title", lang), className="brand"),
                html.P(t("empty_fleet", lang), className="detail-hint"),
                html.Footer(t("disclaimer", lang), className="footer"),
            ],
            className="app-shell",
        )

    ordered = sorted(
        snapshots,
        key=lambda snap: (status_sort_rank(snap["status"]), snap["machine_id"]),
    )
    selected_machine = default_machine or ordered[0]["machine_id"]

    return html.Div(
        [
            html.Header(
                [
                    html.Div(
                        [
                            html.P(
                                t("brand_eyebrow", lang),
                                className="brand-eyebrow",
                                id="brand-eyebrow",
                            ),
                            html.H1(
                                t("app_title", lang),
                                className="brand",
                                id="brand-title",
                            ),
                            html.P(
                                t("tagline", lang),
                                className="tagline",
                                id="brand-tagline",
                            ),
                        ],
                        className="brand-block",
                    ),
                    html.Div(
                        [
                            html.Label(
                                [
                                    html.Span(
                                        t("lang", lang),
                                        id="lang-label",
                                        className="lang-label",
                                    ),
                                    dcc.Dropdown(
                                        id="language-select",
                                        options=language_dropdown_options(),
                                        value=lang,
                                        clearable=False,
                                        searchable=False,
                                        className="language-dropdown",
                                    ),
                                ],
                                className="lang-control",
                            ),
                            html.Span(
                                opcua_banner_text,
                                className="opcua-banner",
                                id="opcua-banner",
                            ),
                        ],
                        className="header-meta",
                    ),
                ],
                className="topbar",
            ),
            html.Div(
                [
                    html.P(
                        floor_summary(snapshots, lang),
                        className="floor-summary",
                        id="floor-summary",
                    ),
                    html.P(
                        t("floor_hint", lang),
                        className="floor-hint",
                        id="floor-hint",
                    ),
                ],
                className="floor-bar",
            ),
            html.Section(
                [
                    machine_card(
                        snap,
                        selected=(snap["machine_id"] == selected_machine),
                        lang=lang,
                    )
                    for snap in ordered
                ],
                className="card-row",
                id="card-row",
                **{"aria-label": t("cards_aria", lang)},
            ),
            html.Section(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H2(
                                        t("panel_main", lang),
                                        className="panel-title",
                                        id="panel-main-title",
                                    ),
                                    html.Span(
                                        id="viewing-pill",
                                        className="viewing-pill",
                                    ),
                                ],
                                className="panel-head",
                            ),
                            dcc.Loading(
                                id="charts-loading",
                                type="dot",
                                color=COLOR_ACCENT,
                                children=html.Div(
                                    [
                                        html.Div(
                                            dcc.Graph(
                                                id="health-graph",
                                                config={"displayModeBar": False},
                                                className="chart-block",
                                            ),
                                            role="img",
                                            id="health-graph-wrap",
                                            **{
                                                "aria-label": t(
                                                    "health_graph_aria", lang
                                                )
                                            },
                                        ),
                                        html.Div(
                                            dcc.Graph(
                                                id="sensor-graph",
                                                config={"displayModeBar": False},
                                                className="chart-block",
                                            ),
                                            role="img",
                                            id="sensor-graph-wrap",
                                            **{
                                                "aria-label": t(
                                                    "sensor_graph_aria", lang
                                                )
                                            },
                                        ),
                                    ],
                                    className="charts-stack",
                                ),
                            ),
                        ],
                        className="panel panel-main",
                    ),
                    html.Div(
                        [
                            html.H2(
                                t("panel_side", lang),
                                className="panel-title",
                                id="panel-side-title",
                            ),
                            html.Div(
                                id="selection-detail",
                                className="selection-detail",
                            ),
                            html.H3(
                                t("panel_notes", lang),
                                className="panel-subtitle",
                                id="panel-notes-title",
                            ),
                            html.Ul(
                                alert_items(alerts, selected_machine, lang),
                                className="alert-feed",
                                id="alert-feed",
                            ),
                        ],
                        className="panel panel-side",
                    ),
                ],
                className="main-grid",
            ),
            html.Footer(t("disclaimer", lang), className="footer", id="app-footer"),
            dcc.Store(id="selected-machine", data=selected_machine),
            dcc.Store(id="alerts-store", data=alerts),
            dcc.Store(id="snapshots-store", data=snapshots),
            dcc.Store(id="opcua-node-count", data=opcua_node_count),
        ],
        className="app-shell",
    )
