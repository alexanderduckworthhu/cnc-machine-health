#!/usr/bin/env python3
"""Train Isolation Forest + write health snapshots / alerts."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.pipeline import run_pipeline


def main() -> None:
    result = run_pipeline(persist=True)
    print(f"Windows: {result['meta']['n_windows']}")
    print(f"Machines: {result['meta']['n_machines']}")
    for snap in result["snapshots"]:
        print(
            f"  {snap['machine_id']}: health={snap['health']} "
            f"status={snap['status']} ttf={snap['ttf_display']}"
        )
    print(f"Alerts: {len(result['alerts'])}")


if __name__ == "__main__":
    main()
