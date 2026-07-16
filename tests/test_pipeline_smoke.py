"""Smoke tests — keep the 2-weekend bar honest."""

from __future__ import annotations

import numpy as np

from src.demo_data import build_demo_fleet
from src.models.health_score import fit_calibration, status_from_health
from src.models.isolation_forest import anomaly_scores, fit_isolation_forest
from src.preprocess.missing import clean_sensor_frame
from src.preprocess.normalize import fit_scaler, transform_sensors
from src.preprocess.windowing import build_windows
from src.ttf import ttf_cycles_from_health


def test_demo_fleet_has_four_machines():
    df = build_demo_fleet()
    assert set(df["machine_id"]) == {"CNC-01", "CNC-02", "CNC-03", "CNC-04"}
    assert df["vibration_rms"].notna().any()


def test_clean_handles_missing():
    df = build_demo_fleet()
    clean = clean_sensor_frame(df)
    assert clean["vibration_rms"].isna().sum() == 0


def test_windows_and_isolation_forest():
    df = clean_sensor_frame(build_demo_fleet())
    scaler = fit_scaler(df)
    scaled = transform_sensors(df, scaler)
    windows, X = build_windows(scaled)
    assert len(X) > 10
    model = fit_isolation_forest(X)
    scores = anomaly_scores(model, X)
    calib = fit_calibration(scores)
    health = calib.health(scores)
    assert health.min() >= 0 and health.max() <= 100
    assert status_from_health(80) == "green"
    assert status_from_health(60) == "amber"
    assert status_from_health(40) == "red"


def test_ttf_monotonic_with_health():
    low = ttf_cycles_from_health(40)
    high = ttf_cycles_from_health(90)
    assert high > low


def test_pipeline_snapshots(tmp_path, monkeypatch):
    from src import config, pipeline

    monkeypatch.setattr(config, "PROCESSED_DIR", tmp_path)
    monkeypatch.setattr(config, "MODEL_DIR", tmp_path)
    monkeypatch.setattr(config, "SNAPSHOTS_PATH", tmp_path / "machine_snapshots.json")
    monkeypatch.setattr(config, "ALERTS_PATH", tmp_path / "alerts.json")
    monkeypatch.setattr(config, "METADATA_PATH", tmp_path / "metadata.json")
    monkeypatch.setattr(config, "MODEL_PATH", tmp_path / "isolation_forest.joblib")
    monkeypatch.setattr(config, "SCALER_PATH", tmp_path / "window_scaler.joblib")
    monkeypatch.setattr(config, "SCORE_CALIB_PATH", tmp_path / "score_calibration.joblib")
    monkeypatch.setattr(pipeline, "PROCESSED_DIR", tmp_path)
    monkeypatch.setattr(pipeline, "SNAPSHOTS_PATH", tmp_path / "machine_snapshots.json")
    monkeypatch.setattr(pipeline, "ALERTS_PATH", tmp_path / "alerts.json")
    monkeypatch.setattr(pipeline, "METADATA_PATH", tmp_path / "metadata.json")
    monkeypatch.setattr(pipeline, "MODEL_PATH", tmp_path / "isolation_forest.joblib")
    monkeypatch.setattr(pipeline, "SCALER_PATH", tmp_path / "window_scaler.joblib")
    monkeypatch.setattr(pipeline, "SCORE_CALIB_PATH", tmp_path / "score_calibration.joblib")

    result = pipeline.run_pipeline(build_demo_fleet(), persist=True)
    assert len(result["snapshots"]) == 4
    assert (tmp_path / "machine_snapshots.json").exists()


def test_opcua_node_ids():
    from src.opcua.mock_server import build_default_server, node_id
    from src.opcua.client import OpcUaClient

    traces = clean_sensor_frame(build_demo_fleet())
    server = build_default_server(traces)
    client = OpcUaClient(server)
    nodes = client.browse("CNC-01")
    assert any("VibrationRMS" in n for n in nodes)
    val = client.read(node_id("CNC-01", "Spindle.VibrationRMS"))
    assert val is None or isinstance(val, (int, float, np.floating))
    assert "mock opc-ua" in client.connection_banner().lower()


def test_human_copy_and_status_mix():
    from src.copy import STATUS_LABEL, floor_summary
    from src.i18n import SUPPORTED_LANGS, t
    from src.pipeline import run_pipeline

    result = run_pipeline(build_demo_fleet(), persist=False)
    statuses = {s["status"] for s in result["snapshots"]}
    assert "green" in statuses
    assert statuses & {"amber", "red"}
    assert STATUS_LABEL["red"] == "Needs a look"
    summary = floor_summary(result["snapshots"])
    assert "Tap a cell" in summary or "look fine" in summary
    assert len(SUPPORTED_LANGS) == 8
    assert t("app_title", "fr") == "Moniteur de broche CNC"
    assert t("status_red", "es") == "Revisar"
    assert "振动" in t("sensor_vibration_rms", "zh")
    assert t("chart_health_title", "ru").startswith("Здоровье")
