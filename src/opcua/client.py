"""
OPC-UA client façade used by the Dash app.

Talks to MockOpcUaServer in this repo. Swap the constructor later for a real
asyncua Client(endpoint) without rewriting the dashboard.
"""

from __future__ import annotations

from typing import Any

from src.copy import opcua_banner
from src.opcua.mock_server import TAG_SUFFIX, MockOpcUaServer, node_id


class OpcUaClient:
    """Thin read/browse wrapper over the in-process mock tag store."""

    def __init__(self, server: MockOpcUaServer) -> None:
        self._server = server
        self.endpoint = server.endpoint

    def browse(self, machine_id: str | None = None) -> list[str]:
        """Return NodeId strings, optionally filtered to one machine."""
        return self._server.browse(machine_id)

    def read(self, node: str) -> Any:
        """Return the current value for a NodeId, or None if missing."""
        node_state = self._server.read(node)
        return None if node_state is None else node_state.value

    def read_sensors(self, machine_id: str) -> dict[str, Any]:
        """Return the latest sensor tag values for one machine."""
        return self._server.read_machine_sensors(machine_id)

    def read_health(self, machine_id: str) -> tuple[float | None, str | None]:
        """Return (health_score, status) tags for one machine."""
        health = self.read(node_id(machine_id, TAG_SUFFIX["health_score"]))
        status = self.read(node_id(machine_id, TAG_SUFFIX["status"]))
        return health, status

    def connection_banner(self) -> str:
        """Return human-readable connection chip text for the header."""
        return opcua_banner(len(self._server.nodes))
