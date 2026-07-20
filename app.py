"""
CNC Spindle Health Monitor: Plotly Dash entrypoint.

Run locally:
  python app.py

Deploy (Render/Railway):
  gunicorn app:server --bind 0.0.0.0:$PORT
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from dash import Dash

from src.config import ASSETS_DIR, DASH_HOST, DASH_PORT, SNAPSHOTS_PATH
from src.copy import APP_TITLE
from src.dashboard.callbacks import register_callbacks
from src.dashboard.layout import build_layout, error_layout
from src.io_utils import ArtefactLoadError
from src.opcua.client import OpcUaClient
from src.opcua.mock_server import build_default_server
from src.pipeline import (
    load_alerts,
    load_clean_traces,
    load_snapshots,
    run_pipeline,
)


def _bootstrap() -> tuple[list[dict[str, Any]], list[dict[str, Any]], str, int]:
    """Load snapshots/alerts and build the mock OPC-UA banner text."""
    if not SNAPSHOTS_PATH.exists():
        run_pipeline(persist=True)
    snapshots = load_snapshots()
    alerts = load_alerts()
    traces = load_clean_traces()
    server = build_default_server(traces)
    for snapshot in snapshots:
        server.publish_health(
            snapshot["machine_id"],
            snapshot["health"],
            snapshot["status"],
        )
    client = OpcUaClient(server)
    return snapshots, alerts, client.connection_banner(), len(server.nodes)


app = Dash(
    __name__,
    assets_folder=str(ASSETS_DIR),
    title=APP_TITLE,
    suppress_callback_exceptions=True,
)
server = app.server

try:
    snapshots, alerts, opcua_banner_text, node_count = _bootstrap()
    app.layout = build_layout(
        snapshots,
        alerts,
        opcua_banner_text,
        opcua_node_count=node_count,
    )
    register_callbacks(app)
except ArtefactLoadError as exc:
    app.layout = error_layout(str(exc))
except (OSError, RuntimeError, ValueError) as exc:
    app.layout = error_layout(str(exc))


if __name__ == "__main__":
    app.run(debug=True, host=DASH_HOST, port=DASH_PORT)
