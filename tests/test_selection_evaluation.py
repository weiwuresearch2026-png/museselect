import pytest

from museselect.boundary import SelectionView
from museselect.evaluation import realized_utility, selection_report
from museselect.selection import freeze_predictions, route_by_centroid


def _rows():
    return [
        {
            "candidate_id": "a::0",
            "source_id": "a",
            "audio_centroid_distance": 0.2,
            "text_centroid_distance": 0.1,
            "interaction_gap": 0.1,
            "log_size": 5.0,
        },
        {
            "candidate_id": "b::0",
            "source_id": "b",
            "audio_centroid_distance": 0.5,
            "text_centroid_distance": 0.4,
            "interaction_gap": 0.2,
            "log_size": 5.0,
        },
    ]


def test_freeze_is_deterministic_except_timestamp():
    view = SelectionView.build("target", "logistic", _rows())
    scores = route_by_centroid(view)
    first = freeze_predictions(view, scores, frozen_at_utc="2026-01-01T00:00:00Z")
    second = freeze_predictions(view, scores, frozen_at_utc="2026-01-02T00:00:00Z")
    assert first.selection_digest == second.selection_digest
    assert first.selected_candidate_id == "a::0"


def test_post_freeze_report():
    view = SelectionView.build("target", "logistic", _rows())
    freeze = freeze_predictions(view, route_by_centroid(view))
    report = selection_report(freeze, {"a::0": 0.02, "b::0": -0.01})
    assert report["top1_regret"] == 0.0
    assert report["harm"] is False
    assert realized_utility([0.5, 0.6], [0.52, 0.61]) == pytest.approx(0.015)
