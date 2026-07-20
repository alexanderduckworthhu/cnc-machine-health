"""Typed file I/O helpers, never fail silently."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

logger = logging.getLogger(__name__)


class ArtefactLoadError(RuntimeError):
    """Raised when a required demo artefact cannot be read."""


def read_json(path: Path) -> Any:
    """Load JSON from disk; raise ArtefactLoadError with path context on failure."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ArtefactLoadError(f"Missing artefact: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ArtefactLoadError(f"Corrupt JSON in {path}: {exc}") from exc
    except OSError as exc:
        raise ArtefactLoadError(f"Cannot read {path}: {exc}") from exc


def write_json(path: Path, payload: Any) -> None:
    """Write JSON to disk; raise ArtefactLoadError with path context on failure."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    except OSError as exc:
        raise ArtefactLoadError(f"Cannot write {path}: {exc}") from exc


def read_csv(path: Path) -> pd.DataFrame:
    """Load a CSV; raise ArtefactLoadError with path context on failure."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError as exc:
        raise ArtefactLoadError(f"Missing CSV: {path}") from exc
    except pd.errors.EmptyDataError as exc:
        raise ArtefactLoadError(f"Empty CSV: {path}") from exc
    except pd.errors.ParserError as exc:
        raise ArtefactLoadError(f"Unreadable CSV {path}: {exc}") from exc
    except OSError as exc:
        raise ArtefactLoadError(f"Cannot read CSV {path}: {exc}") from exc


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    """Write a DataFrame to CSV; raise ArtefactLoadError on failure."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        frame.to_csv(path, index=False)
    except OSError as exc:
        raise ArtefactLoadError(f"Cannot write CSV {path}: {exc}") from exc


def dump_joblib(path: Path, obj: Any) -> None:
    """Serialize an object with joblib; raise ArtefactLoadError on failure."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(obj, path)
    except OSError as exc:
        raise ArtefactLoadError(f"Cannot write model artefact {path}: {exc}") from exc


def load_joblib(path: Path) -> Any:
    """Deserialize a joblib artefact; raise ArtefactLoadError on failure."""
    try:
        return joblib.load(path)
    except FileNotFoundError as exc:
        raise ArtefactLoadError(f"Missing model artefact: {path}") from exc
    except OSError as exc:
        raise ArtefactLoadError(f"Cannot read model artefact {path}: {exc}") from exc
    except Exception as exc:  # joblib can raise various pickle errors
        raise ArtefactLoadError(f"Corrupt model artefact {path}: {exc}") from exc
