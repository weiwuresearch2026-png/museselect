import pytest

from museselect.boundary import CandidateRecord, SelectionView


BASE = {
    "candidate_id": "a::0",
    "source_id": "a",
    "audio_centroid_distance": 0.3,
    "text_centroid_distance": 0.2,
    "interaction_gap": 0.1,
    "log_size": 5.0,
}


def test_sealed_field_is_rejected():
    with pytest.raises(ValueError, match="sealed fields"):
        CandidateRecord.from_mapping({**BASE, "realized_utility": 0.4})


def test_duplicate_candidate_is_rejected():
    with pytest.raises(ValueError, match="unique"):
        SelectionView.build("target", "learner", [BASE, BASE])

