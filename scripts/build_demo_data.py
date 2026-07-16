#!/usr/bin/env python3
"""Generate synthetic CMAPSS-proxy CNC sensor traces."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.config import SAMPLE_DIR
from src.demo_data import save_demo_sample


def main() -> None:
    path = save_demo_sample(SAMPLE_DIR)
    print(f"Wrote demo sensor traces → {path}")


if __name__ == "__main__":
    main()
