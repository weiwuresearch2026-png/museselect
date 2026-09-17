"""Deterministic routing and immutable prediction-freeze records."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Mapping

from .boundary import SelectionView


@dataclass(frozen=True)
class FreezeRecord:
    target_id: str
    learner_id: str
    selected_candidate_id: str
    selected_source_id: str
    scores: Mapping[str, float]
    selection_digest: str
    frozen_at_utc: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def route_by_centroid(view: SelectionView) -> dict[str, float]:
    """Public baseline: smaller joint centroid distance receives a higher score."""
    return {
        row.candidate_id: -(
            row.audio_centroid_distance + row.text_centroid_distance
        )
        / 2.0
        for row in view.candidates
    }


def freeze_predictions(
    view: SelectionView,
    scores: Mapping[str, float],
    *,
    frozen_at_utc: str | None = None,
) -> FreezeRecord:
    expected = {row.candidate_id for row in view.candidates}
    if set(scores) != expected:
        raise ValueError("scores must contain exactly the candidates in SelectionView")
    ordered = sorted((key, float(value)) for key, value in scores.items())
    selected_id = max(ordered, key=lambda item: (item[1], item[0]))[0]
    source_by_candidate = {
        row.candidate_id: row.source_id for row in view.candidates
    }
    payload = {
        "target_id": view.target_id,
        "learner_id": view.learner_id,
        "scores": ordered,
        "selected_candidate_id": selected_id,
    }
    digest = sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    timestamp = frozen_at_utc or datetime.now(timezone.utc).isoformat()
    return FreezeRecord(
        target_id=view.target_id,
        learner_id=view.learner_id,
        selected_candidate_id=selected_id,
        selected_source_id=source_by_candidate[selected_id],
        scores=dict(ordered),
        selection_digest=digest,
        frozen_at_utc=timestamp,
    )

