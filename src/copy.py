"""
Compatibility helpers over src.i18n for pipeline (English artefact storage).

Dashboard code should call src.i18n.t / status_label directly with the UI language.
"""

from __future__ import annotations

from typing import Any

from src.i18n import DEFAULT_LANG, t


def floor_summary(snapshots: list[dict[str, Any]], lang: str = DEFAULT_LANG) -> str:
    """Return a one-line floor triage summary for the header bar."""
    n_red = sum(1 for s in snapshots if s.get("status") == "red")
    n_amber = sum(1 for s in snapshots if s.get("status") == "amber")
    if n_red == 0 and n_amber == 0:
        return t("floor_all_fine", lang)
    parts: list[str] = []
    if n_red == 1:
        parts.append(t("floor_need_look_1", lang))
    elif n_red > 1:
        parts.append(t("floor_need_look_n", lang, n=n_red))
    if n_amber == 1:
        parts.append(t("floor_watch_1", lang))
    elif n_amber > 1:
        parts.append(t("floor_watch_n", lang, n=n_amber))
    return " · ".join(parts) + " " + t("floor_tap", lang)


def alert_message(
    machine_id: str,
    health: float,
    status: str,
    ttf_display: str,
    lang: str = DEFAULT_LANG,
) -> str:
    """Return a maintenance note for amber/red cells."""
    key = "alert_red" if status == "red" else "alert_amber"
    return t(key, lang, machine_id=machine_id, health=health, ttf=ttf_display)


def drop_alert_message(
    machine_id: str,
    previous_health: float,
    health: float,
    lang: str = DEFAULT_LANG,
) -> str:
    """Return a note when health falls sharply between consecutive windows."""
    return t(
        "alert_drop",
        lang,
        machine_id=machine_id,
        delta=previous_health - health,
        prev=previous_health,
        health=health,
    )


def opcua_banner(n_nodes: int, lang: str = DEFAULT_LANG) -> str:
    """Return the OPC-UA connection chip text for the header."""
    return t("opcua_banner", lang, n=n_nodes)


def detail_health_line(
    health: float,
    status: str,
    ttf_display: str,
    lang: str = DEFAULT_LANG,
) -> str:
    """Return the selected-cell health sentence for the side panel."""
    from src.i18n import status_label

    return t(
        "detail_health",
        lang,
        health=health,
        status=status_label(status, lang),
        ttf=ttf_display,
    )


def empty_alerts_floor(lang: str = DEFAULT_LANG) -> str:
    """Return copy when the floor has no maintenance notes."""
    return t("empty_alerts_floor", lang)


def machine_card_aria(
    machine_id: str,
    status: str,
    health: float,
    lang: str = DEFAULT_LANG,
) -> str:
    """Return an accessible name for a machine card button."""
    return t(
        "card_aria",
        lang,
        machine_id=machine_id,
        status=t(f"aria_{status}", lang),
        health=health,
    )


def viewing_pill(machine_id: str, lang: str = DEFAULT_LANG) -> str:
    """Return the compact ‘viewing’ chip next to the main panel title."""
    return t("viewing_pill", lang, machine_id=machine_id)


def empty_alerts_for_machine(machine_id: str, lang: str = DEFAULT_LANG) -> str:
    """Return copy when the selected cell has no notes."""
    return t("empty_alerts_machine", lang, machine_id=machine_id)


# Legacy module-level constants (English) for older imports / tests.
APP_TITLE = t("app_title")
BRAND_EYEBROW = t("brand_eyebrow")
TAGLINE = t("tagline")
FLOOR_HINT = t("floor_hint")
PANEL_MAIN_TITLE = t("panel_main")
PANEL_SIDE_TITLE = t("panel_side")
PANEL_NOTES_SUBTITLE = t("panel_notes")
SENSOR_DETAILS_SUMMARY = t("sensor_details")
CARD_CTA = t("card_cta")
CARD_CTA_SELECTED = t("card_cta_selected")
CARD_TOOLTIP = t("card_tooltip")
VIEWING_PILL = t("viewing_pill", machine_id="{machine_id}")
ROUGHLY_LEFT_PREFIX = t("roughly_left_prefix")
ROUGHLY_LEFT_SUFFIX = t("roughly_left_suffix")
HEALTH_DENOMINATOR = t("health_denom")
CHART_HEALTH_TITLE = t("chart_health_title")
CHART_SENSOR_TITLE = t("chart_sensor_title")
CHART_EMPTY_HEALTH = t("chart_empty_health")
CHART_EMPTY_SENSORS = t("chart_empty_sensors")
CHART_AXIS_CYCLE = t("chart_axis_cycle")
CHART_AXIS_HEALTH = t("chart_axis_health")
SUBPLOT_VIBRATION = t("subplot_vibration")
SUBPLOT_TEMPERATURE = t("subplot_temperature")
SUBPLOT_CURRENT_LOAD = t("subplot_current_load")
STATUS_LABEL = {
    "green": t("status_green"),
    "amber": t("status_amber"),
    "red": t("status_red"),
}
STATUS_HINT = {
    "green": t("hint_green"),
    "amber": t("hint_amber"),
    "red": t("hint_red"),
}
STATUS_ARIA = {
    "green": t("aria_green"),
    "amber": t("aria_amber"),
    "red": t("aria_red"),
}
SEVERITY_LABEL = {
    "high": t("sev_high"),
    "medium": t("sev_medium"),
    "low": t("sev_low"),
}
BOOTSTRAP_ERROR_TITLE = t("bootstrap_error_title")
BOOTSTRAP_ERROR_HINT = t("bootstrap_error_hint")
EMPTY_FLEET = t("empty_fleet")
EMPTY_ALERTS_FLOOR = t("empty_alerts_floor")
EMPTY_ALERTS_MACHINE = t("empty_alerts_machine", machine_id="{machine_id}")
DISCLAIMER = t("disclaimer")
DISCLAIMER_HUMAN = DISCLAIMER
