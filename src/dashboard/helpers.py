"""Shared dashboard helpers."""

from __future__ import annotations

STATUS_SORT_RANK = {"red": 0, "amber": 1, "green": 2}


def status_sort_rank(status: str) -> int:
    """Return sort rank so red cells appear before amber before green."""
    return STATUS_SORT_RANK.get(status, 9)
