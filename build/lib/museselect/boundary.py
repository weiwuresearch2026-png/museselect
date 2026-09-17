"""Selection-time schema enforcing the paper's information boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping


FORBIDDEN_SELECTION_FIELDS = frozenset(
    {
        "utility",
        "realized_utility",
        "transfer_gain",
        "validation_label",
        "validation_labels",
        "test_label",
        "test_labels",
        "test_score",
        "oracle_rank",
    }
)


@dataclass(frozen=True)
class CandidateRecord:
    """Aggregate source--target evidence available before candidate training."""

    candidate_id: str
    source_id: str
    audio_centroid_distance: float
    text_centroid_distance: float
    interaction_gap: float
    log_size: float
    missing_rate: float = 0.0

    @classmethod
    def from_mapping(cls, row: Mapping[str, Any]) -> "CandidateRecord":
        leaked = sorted(FORBIDDEN_SELECTION_FIELDS.intersection(row))
        if leaked:
            raise ValueError(
                "selection-time record contains sealed fields: " + ", ".join(leaked)
            )
        required = {
            "candidate_id",
            "source_id",
            "audio_centroid_distance",
            "text_centroid_distance",
            "interaction_gap",
            "log_size",
        }
        missing = sorted(required.difference(row))
        if missing:
            raise ValueError("missing selection fields: " + ", ".join(missing))
        record = cls(
            candidate_id=str(row["candidate_id"]),
            source_id=str(row["source_id"]),
            audio_centroid_distance=float(row["audio_centroid_distance"]),
            text_centroid_distance=float(row["text_centroid_distance"]),
            interaction_gap=float(row["interaction_gap"]),
            log_size=float(row["log_size"]),
            missing_rate=float(row.get("missing_rate", 0.0)),
        )
        if not 0.0 <= record.missing_rate <= 1.0:
            raise ValueError("missing_rate must lie in [0, 1]")
        if not record.candidate_id or not record.source_id:
            raise ValueError("candidate_id and source_id must be non-empty")
        return record


@dataclass(frozen=True)
class SelectionView:
    """Immutable collection visible to the selector before evaluation is opened."""

    target_id: str
    learner_id: str
    candidates: tuple[CandidateRecord, ...]

    @classmethod
    def build(
        cls,
        target_id: str,
        learner_id: str,
        rows: Iterable[Mapping[str, Any]],
    ) -> "SelectionView":
        candidates = tuple(CandidateRecord.from_mapping(row) for row in rows)
        if not candidates:
            raise ValueError("at least one candidate is required")
        ids = [record.candidate_id for record in candidates]
        if len(ids) != len(set(ids)):
            raise ValueError("candidate_id values must be unique")
        return cls(str(target_id), str(learner_id), candidates)

