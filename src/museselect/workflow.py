"""Staged source routing and probe-based shortlist construction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np

from .boundary import SelectionView


@dataclass(frozen=True)
class StagedShortlist:
    selected_source_id: str
    candidate_ids: tuple[str, ...]
    source_scores: Mapping[str, float]


def route_source_by_centroid(view: SelectionView) -> dict[str, float]:
    """Average negative joint-centroid distance over buckets in each source."""
    grouped: dict[str, list[float]] = {}
    for row in view.candidates:
        grouped.setdefault(row.source_id, []).append(
            -(row.audio_centroid_distance + row.text_centroid_distance) / 2.0
        )
    return {source: float(np.mean(scores)) for source, scores in grouped.items()}


def build_staged_shortlist(
    view: SelectionView,
    probe_scores: Mapping[str, float],
    *,
    k: int,
) -> StagedShortlist:
    """Route one source statically, then keep its top-k probe-scored buckets."""
    expected = {row.candidate_id for row in view.candidates}
    if set(probe_scores) != expected:
        raise ValueError("probe_scores must contain exactly the visible candidates")
    if not 1 <= k <= len(view.candidates):
        raise ValueError("k must be between one and the number of candidates")
    source_scores = route_source_by_centroid(view)
    selected_source = max(source_scores.items(), key=lambda item: (item[1], item[0]))[0]
    allowed = {
        row.candidate_id for row in view.candidates if row.source_id == selected_source
    }
    ranked = sorted(allowed, key=lambda key: (float(probe_scores[key]), key), reverse=True)
    return StagedShortlist(
        selected_source_id=selected_source,
        candidate_ids=tuple(ranked[: min(k, len(ranked))]),
        source_scores=source_scores,
    )
