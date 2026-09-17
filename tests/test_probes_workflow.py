import numpy as np

from museselect.boundary import SelectionView
from museselect.probes import leep_score, logme_score
from museselect.workflow import build_staged_shortlist, route_source_by_centroid


def test_probe_scores_are_finite():
    probabilities = np.asarray([
        [0.8, 0.1, 0.1], [0.1, 0.8, 0.1], [0.1, 0.2, 0.7],
        [0.7, 0.2, 0.1], [0.2, 0.7, 0.1], [0.1, 0.1, 0.8],
    ])
    labels = np.asarray([0, 1, 2, 0, 1, 2])
    assert np.isfinite(leep_score(probabilities, labels))
    assert np.isfinite(logme_score(np.log(probabilities), labels))


def test_route_then_shortlist():
    rows = [
        {"candidate_id": "near::0", "source_id": "near", "audio_centroid_distance": .1, "text_centroid_distance": .2, "interaction_gap": .1, "log_size": 5},
        {"candidate_id": "near::1", "source_id": "near", "audio_centroid_distance": .2, "text_centroid_distance": .2, "interaction_gap": .1, "log_size": 5},
        {"candidate_id": "far::0", "source_id": "far", "audio_centroid_distance": .7, "text_centroid_distance": .6, "interaction_gap": .1, "log_size": 5},
        {"candidate_id": "far::1", "source_id": "far", "audio_centroid_distance": .8, "text_centroid_distance": .6, "interaction_gap": .1, "log_size": 5},
    ]
    view = SelectionView.build("target", "logistic", rows)
    assert max(route_source_by_centroid(view), key=route_source_by_centroid(view).get) == "near"
    result = build_staged_shortlist(
        view, {"near::0": .2, "near::1": .9, "far::0": 2, "far::1": 3}, k=1
    )
    assert result.selected_source_id == "near"
    assert result.candidate_ids == ("near::1",)
