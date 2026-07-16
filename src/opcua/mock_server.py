"""
Mock OPC-UA server / tag store for portfolio demos.

Good-enough bar (2 weekends):
  - Realistic node IDs: ns=2;s=CNC-01.Spindle.VibrationRMS
  - A client API that looks like industrial middleware (read / browse / subscribe stub)
  - Values fed from the processed sensor CSV — NOT a live asyncua TCP server by default

Over-engineer trap:
  - Standing up real asyncua + certificates + Docker networking for a hiring demo
  - Pretending you integrated with a Swatch Group plant network

Interview line:
  "The dashboard reads through an OPC-UA-shaped abstraction. In production that
   client would point at Kepware/TwinCAT; here it reads a replay buffer so the
   architecture story is visible without plant access."
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

import pandas as pd

from src.config import (
    MACHINE_IDS,
    OPCUA_ENDPOINT,
    OPCUA_NAMESPACE,
    SENSOR_COLUMNS,
    SENSOR_DISPLAY,
)


def node_id(machine_id: str, tag: str) -> str:
    """Browse-path style NodeId string."""
    return f"ns={OPCUA_NAMESPACE};s={machine_id}.{tag}"


# Tag tree mirrors a spindle condition-monitoring folder.
TAG_SUFFIX: dict[str, str] = {
    "vibration_rms": "Spindle.VibrationRMS",
    "vibration_peak": "Spindle.VibrationPeak",
    "temperature_spindle_c": "Spindle.Temperature",
    "temperature_coolant_c": "Coolant.Temperature",
    "current_draw_a": "Spindle.Current",
    "load_pct": "Axis.LoadPct",
    "health_score": "Health.Score",
    "status": "Health.Status",
}


@dataclass
class OpcUaNode:
    node_id: str
    display_name: str
    value: Any
    timestamp: datetime
    quality: str = "Good"


@dataclass
class MockOpcUaServer:
    """In-process OPC-UA-shaped tag store backed by a sensor replay buffer."""

    endpoint: str = OPCUA_ENDPOINT
    nodes: dict[str, OpcUaNode] = field(default_factory=dict)
    _cursor: dict[str, int] = field(default_factory=dict)
    _frames: dict[str, pd.DataFrame] = field(default_factory=dict)

    def register_machine_trace(self, machine_id: str, traces: pd.DataFrame) -> None:
        """Register one machine's sensor history and publish the latest sample."""
        machine_frame = (
            traces[traces["machine_id"] == machine_id]
            .sort_values("cycle")
            .reset_index(drop=True)
        )
        self._frames[machine_id] = machine_frame
        self._cursor[machine_id] = max(len(machine_frame) - 1, 0)
        self._publish_row(machine_id, self._cursor[machine_id])

    def _publish_row(self, machine_id: str, idx: int) -> None:
        g = self._frames[machine_id]
        row = g.iloc[idx]
        now = datetime.now(timezone.utc)
        for col in SENSOR_COLUMNS:
            if col not in row.index:
                continue
            nid = node_id(machine_id, TAG_SUFFIX[col])
            self.nodes[nid] = OpcUaNode(
                node_id=nid,
                display_name=SENSOR_DISPLAY.get(col, col),
                value=float(row[col]) if pd.notna(row[col]) else None,
                timestamp=now,
            )
        # Health tags filled by dashboard/pipeline after scoring
        for tag in ("health_score", "status"):
            nid = node_id(machine_id, TAG_SUFFIX[tag])
            if nid not in self.nodes:
                self.nodes[nid] = OpcUaNode(
                    node_id=nid,
                    display_name=tag,
                    value=None,
                    timestamp=now,
                )

    def publish_health(self, machine_id: str, health: float, status: str) -> None:
        now = datetime.now(timezone.utc)
        self.nodes[node_id(machine_id, TAG_SUFFIX["health_score"])] = OpcUaNode(
            node_id=node_id(machine_id, TAG_SUFFIX["health_score"]),
            display_name="Health score",
            value=round(float(health), 1),
            timestamp=now,
        )
        self.nodes[node_id(machine_id, TAG_SUFFIX["status"])] = OpcUaNode(
            node_id=node_id(machine_id, TAG_SUFFIX["status"]),
            display_name="Health status",
            value=status,
            timestamp=now,
        )

    def browse(self, machine_id: str | None = None) -> list[str]:
        ids = sorted(self.nodes.keys())
        if machine_id:
            needle = f";s={machine_id}."
            ids = [n for n in ids if needle in n]
        return ids

    def read(self, node: str) -> OpcUaNode | None:
        return self.nodes.get(node)

    def read_machine_sensors(self, machine_id: str) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for col, suffix in TAG_SUFFIX.items():
            if col in ("health_score", "status"):
                continue
            n = self.read(node_id(machine_id, suffix))
            out[col] = None if n is None else n.value
        return out

    def step(self, machine_id: str, delta: int = 1) -> None:
        """Advance the replay cursor (simulates a new OPC-UA sample)."""
        if machine_id not in self._frames:
            return
        n = len(self._frames[machine_id])
        self._cursor[machine_id] = min(max(self._cursor[machine_id] + delta, 0), n - 1)
        self._publish_row(machine_id, self._cursor[machine_id])


def build_default_server(traces: pd.DataFrame) -> MockOpcUaServer:
    server = MockOpcUaServer()
    for mid in MACHINE_IDS:
        if mid in set(traces["machine_id"]):
            server.register_machine_trace(mid, traces)
    return server
